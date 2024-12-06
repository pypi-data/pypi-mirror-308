import os
import traceback
from functools import partial
from multiprocessing import Manager
from typing import TYPE_CHECKING

import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import pyqtgraph as pg
from qtpy.QtCore import QThreadPool
from qtpy.QtWidgets import QSizePolicy, QVBoxLayout, QWidget
from scipy.optimize import curve_fit

if TYPE_CHECKING:
    import napari

import trackpy as tp

from smlmlab.gui import Ui_Frame as gui
from smlmlab.utils.compute_utils import _utils_compute
from smlmlab.utils.events_utils import _events_utils
from smlmlab.utils.import_utils import _import_utils
from smlmlab.utils.loc_utils import _loc_utils
from smlmlab.utils.picasso_utils import _picasso_detect_utils
from smlmlab.utils.plot_utils import CustomMatplotlibWidget, _plot_utils
from smlmlab.utils.undrift_utils import _undrift_utils
from smlmlab.utils.viewer_utils import _viewer_utils


class QWidget(QWidget, gui, _import_utils,
    _events_utils, _picasso_detect_utils, _loc_utils,
    _viewer_utils, _utils_compute, _undrift_utils, _plot_utils, ):

    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self.viewer = viewer

        self.gui = gui()
        self.gui.setupUi(self)

        # create pyqt graph container
        self.graph_container = self.gui.graph_container
        self.graph_container.setLayout(QVBoxLayout())

        self.graph_canvas = pg.GraphicsLayoutWidget()
        self.graph_container.layout().addWidget(self.graph_canvas)

        # create pyqt graph container

        self.filter_graph_container = self.gui.filter_graph_container
        self.filter_graph_container.setLayout(QVBoxLayout())

        self.filter_graph_canvas = pg.GraphicsLayoutWidget()
        self.filter_graph_container.layout().addWidget(self.filter_graph_canvas)

        # create pyqt graph container
        self.lifetime_graph = self.gui.lifetime_graph
        self.lifetime_graph.setLayout(QVBoxLayout())
        self.lifetime_graph.setMinimumWidth(100)

        self.lifetime_graph_canvas = CustomMatplotlibWidget(self)
        self.lifetime_graph.layout().addWidget(self.lifetime_graph_canvas)
        self.lifetime_graph_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lifetime_graph_canvas.axes.clear()

        self.gui.import_data.clicked.connect(self.import_image_data)

        self.viewer.dims.events.current_step.connect(partial(self.draw_molecules, update_vis=False))

        self.gui.picasso_detect.clicked.connect(partial(self.pixseq_picasso, detect=True, fit=False))
        self.gui.picasso_fit.clicked.connect(partial(self.pixseq_picasso, detect=False, fit=True))
        self.gui.picasso_detectfit.clicked.connect(partial(self.pixseq_picasso, detect=True, fit=True))
        self.gui.picasso_render.clicked.connect(self.picasso_render)
        self.gui.export_locs.clicked.connect(self.initialise_export_locs)

        self.gui.picasso_undrift.clicked.connect(self.initialise_undrift)

        self.gui.picasso_vis_mode.currentIndexChanged.connect(partial(self.draw_molecules, update_vis=True))
        self.gui.picasso_vis_mode.currentIndexChanged.connect(partial(self.draw_bounding_boxes, update_vis=True))
        self.gui.picasso_vis_size.currentIndexChanged.connect(partial(self.draw_molecules, update_vis=True))
        self.gui.picasso_vis_size.currentIndexChanged.connect(partial(self.draw_bounding_boxes, update_vis=True))
        self.gui.picasso_vis_opacity.currentIndexChanged.connect(partial(self.draw_molecules, update_vis=True))
        self.gui.picasso_vis_opacity.currentIndexChanged.connect(partial(self.draw_bounding_boxes, update_vis=True))
        self.gui.picasso_vis_edge_width.currentIndexChanged.connect(partial(self.draw_molecules, update_vis=True))
        self.gui.picasso_vis_edge_width.currentIndexChanged.connect(partial(self.draw_bounding_boxes, update_vis=True))

        self.gui.picasso_dataset.currentIndexChanged.connect(lambda: self.update_channel_selector(dataset_selector="picasso_dataset", channel_selector="picasso_channel", ))
        self.gui.picasso_render_dataset.currentIndexChanged.connect(lambda: self.update_channel_selector(dataset_selector="picasso_render_dataset", channel_selector="picasso_render_channel", ))
        self.gui.plot_dataset.currentIndexChanged.connect(lambda: self.update_channel_selector(dataset_selector="plot_dataset", channel_selector="plot_channel", efficiency=True, ))
        self.gui.locs_export_dataset.currentIndexChanged.connect(lambda: self.update_channel_selector(dataset_selector="locs_export_dataset", channel_selector="locs_export_channel", ))
        self.gui.picasso_undrift_dataset.currentIndexChanged.connect(lambda: self.update_channel_selector(dataset_selector="picasso_undrift_dataset", channel_selector="picasso_undrift_channel", ))

        self.gui.plot_mode.currentIndexChanged.connect(self.update_plot_channel)
        self.gui.plot_dataset.currentIndexChanged.connect(self.draw_line_plot)
        self.gui.plot_channel.currentIndexChanged.connect(self.draw_line_plot)
        self.gui.subtract_background.clicked.connect(self.draw_line_plot)
        self.gui.export_profile_data.clicked.connect(self.export_profile_data)

        self.gui.add_line.clicked.connect(lambda: self.draw_shapes(mode="line"))
        self.gui.add_box.clicked.connect(lambda: self.draw_shapes(mode="box"))
        self.gui.add_background.clicked.connect(lambda: self.draw_shapes(mode="background"))

        self.gui.dataset_selector.currentIndexChanged.connect(partial(self.update_active_image, dataset=self.gui.dataset_selector.currentText(), ))

        self.gui.plot_lifetime_hist.clicked.connect(self.plot_lifetime_histogram)
        self.gui.export_lifetime_data.clicked.connect(self.export_lifetime_data)

        self.gui.picasso_filter_dataset.currentIndexChanged.connect(self.update_filter_criterion)
        self.gui.picasso_filter_channel.currentIndexChanged.connect(self.update_filter_criterion)
        self.gui.filter_criterion.currentIndexChanged.connect(self.update_criterion_ranges)
        self.gui.filter_localisations.clicked.connect(self.filter_localisations)


        self.verbose = False

        self.dataset_dict = {}
        self.localisation_dict = {"bounding_boxes": {}, "molecules": {}}
        self.traces_dict = {}
        self.plot_dict = {}
        self.contrast_dict = {}

        self.active_dataset = None
        self.active_channel = None

        self.threadpool = QThreadPool()

        manager = Manager()
        self.stop_event = manager.Event()

        self.worker = None
        self.multiprocessing_active = False

        self.viewer.layers.events.inserted.connect(self.on_add_layer)

        # keybind F1

        self.viewer.bind_key("f", func = self.update_filter_criterion, overwrite = True)



    def filter_localisations(self, viewer=None):

        try:

            dataset = self.gui.picasso_filter_dataset.currentText()
            channel = self.gui.picasso_filter_channel.currentText()
            criterion = self.gui.filter_criterion.currentText()
            min_value = self.gui.filter_min.value()
            max_value = self.gui.filter_max.value()

            if dataset != "" and channel != "":
                loc_dict, n_locs, fitted = self.get_loc_dict(dataset, channel.lower(), type="molecules")

                if n_locs > 0:

                    locs = loc_dict["localisations"].copy()

                    columns = list(locs.dtype.names)

                    if criterion in columns:

                        self.gui.filter_localisations.setEnabled(False)

                        n_locs = len(locs)

                        locs = locs[locs[criterion] > min_value]
                        locs = locs[locs[criterion] < max_value]

                        n_filtered = len(locs)

                        if n_filtered < n_locs:

                            n_removed = n_locs - n_filtered

                            render_locs = {}

                            for frame in np.unique(locs["frame"]):
                                frame_locs = locs[locs["frame"] == frame].copy()
                                render_locs[frame] = np.vstack((frame_locs.y, frame_locs.x)).T.tolist()

                            loc_dict["localisations"] = locs
                            loc_dict["render_locs"] = render_locs

                            self.localisation_dict["molecules"][dataset][channel.lower()] = loc_dict

                            self.draw_molecules(update_vis=True)
                            self.update_criterion_ranges()

                            print(f"Filtered {n_removed} localisations")

            self.gui.filter_localisations.setEnabled(True)

        except:
            self.gui.filter_localisations.setEnabled(True)
            print(traceback.format_exc())


    def update_filter_criterion(self, viewer=None):


        try:

            columns = []

            dataset = self.gui.picasso_filter_dataset.currentText()
            channel = self.gui.picasso_filter_channel.currentText()
            selector = self.gui.filter_criterion

            if dataset != "" and channel != "":
                loc_dict, n_locs, fitted = self.get_loc_dict(dataset, channel.lower(), type="molecules")

                if n_locs > 0:

                    locs = loc_dict["localisations"].copy()

                    columns = list(locs.dtype.names)

            selector.blockSignals(True)
            selector.clear()
            selector.blockSignals(False)

            if len(columns) > 0:
                selector.addItems(columns)

        except:
            print(traceback.format_exc())


    def update_criterion_ranges(self, viewer=None, plot=True):

        try:
            columns = []

            dataset = self.gui.picasso_filter_dataset.currentText()
            channel = self.gui.picasso_filter_channel.currentText()
            criterion = self.gui.filter_criterion.currentText()

            if dataset != "" and channel != "":
                loc_dict, n_locs, fitted = self.get_loc_dict(dataset, channel.lower(), type="molecules")

                if n_locs > 0:

                    locs = loc_dict["localisations"].copy()

                    columns = list(locs.dtype.names)

                    if criterion in columns:

                        values = locs[criterion]

                        if plot:
                            self.plot_filter_graph(criterion, values)

                        min_value = np.min(values)
                        max_value = np.max(values)

                        self.gui.filter_min.setMinimum(min_value)
                        self.gui.filter_min.setMaximum(max_value)

                        self.gui.filter_max.setMinimum(min_value)
                        self.gui.filter_max.setMaximum(max_value)

                        self.gui.filter_min.setValue(min_value)
                        self.gui.filter_max.setValue(max_value)

        except:
            print(traceback.format_exc())

    def plot_filter_graph(self, criterion = "", values = None):

        try:
            self.filter_graph_canvas.clear()

            if values is not None:

                values = values[~np.isnan(values)]

                if len(values) > 0:
                    ax = self.filter_graph_canvas.addPlot()

                    # Create histogram
                    y, x = np.histogram(values, bins=100)

                    ax.plot(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 75))
                    ax.setLabel('bottom', f"{criterion} values")
                    ax.setLabel('left', 'Frequency')

        except:
            print(traceback.format_exc())



    def increment_file_path(self, path):

        base, ext = os.path.splitext(path)

        if os.path.exists(path):
            i = 1
            while os.path.exists(f"{base}_{i}{ext}"):
                i += 1

            path = f"{base}_{i}{ext}"

        return path

    def export_profile_data(self, viewer=None):

        try:

            plot_data = self.get_plot_data()

            if plot_data != {}:

                channel = self.gui.plot_channel.currentText()
                dataset = self.gui.plot_dataset.currentText()
                mode_index = self.gui.plot_mode.currentIndex()

                if channel not in self.dataset_dict[dataset].keys():
                    export_channel = channel
                    channel = list(self.dataset_dict[dataset].keys())[0]
                else:
                    export_channel = channel

                export_channel = export_channel.replace(" ", "")

                import_path = self.dataset_dict[dataset][channel.lower()]["path"]
                base, ext = os.path.splitext(import_path)

                if mode_index == 0:
                    export_path = base + f"_{export_channel}_line_profile.csv"
                elif mode_index == 1:
                    export_path = base + f"_{export_channel}_line_profile.csv"

                    y_data = list(plot_data.values())[0]
                    x_data = np.arange(len(y_data))

                    fitX, fitY, peak_width = self.fit_custom_gaussian(x_data, y_data, upscale=False)
                    plot_data["Gaussian fit"] = fitY

                else:
                    export_path = base + f"_{export_channel}_time_series.csv"

                export_path = self.increment_file_path(export_path)

                plot_data = pd.DataFrame(plot_data)

                plot_data.to_csv(export_path, index=False)

                print(f"Exported profile data to {export_path}")

        except:
            print(traceback.format_exc())


    def export_lifetime_data(self, viewer=None):
        try:
            dataset = self.gui.lifetimes_dataset.currentText()
            channel = self.gui.lifetimes_channel.currentText()

            if dataset != "" and channel != "":
                import_path = self.dataset_dict[dataset][channel.lower()]["path"]
                base, ext = os.path.splitext(import_path)

                lifetime_path = base + "_lifetimes.csv"

                lifetime_path = self.increment_file_path(lifetime_path)

                lifetimes = self.get_lifetimes()

                if len(lifetimes) > 0:
                    np.savetxt(lifetime_path, lifetimes, delimiter=",")

                    print(f"Exported lifetime data to {lifetime_path}")

        except:
            print(traceback.format_exc())

    def get_lifetimes(self):
        lifetimes = []

        try:
            dataset = self.gui.lifetimes_dataset.currentText()
            channel = self.gui.lifetimes_channel.currentText()

            if dataset != "" and channel != "":
                loc_dict, n_locs, fitted = self.get_loc_dict(dataset, channel.lower(), type="molecules")

                if n_locs > 0:
                    min_lifetime = int(self.gui.min_lifetime.text())
                    max_lifetime = int(self.gui.max_lifetime.text())

                    locs = loc_dict["localisations"].copy()

                    columns = list(locs.dtype.names)

                    df = pd.DataFrame(locs, columns=columns)

                    # Link particles across frames
                    tracked = tp.link(df, search_range=2, memory=1)

                    lifetimes = tracked["particle"].value_counts().to_numpy()

                    lifetimes = lifetimes[lifetimes > min_lifetime]
                    lifetimes = lifetimes[lifetimes < max_lifetime]

        except:
            print(traceback.format_exc())

        return lifetimes

    def plot_lifetime_histogram(self, viewer=None):
        try:
            dataset = self.gui.lifetimes_dataset.currentText()
            channel = self.gui.lifetimes_channel.currentText()
            lifetime_bins = int(self.gui.lifetime_bins.text())
            fit_exponential = self.gui.fit_exponential.isChecked()
            min_lifetime = int(self.gui.min_lifetime.text())
            max_lifetime = int(self.gui.max_lifetime.text())

            if dataset != "" and channel != "":
                loc_dict, n_locs, fitted = self.get_loc_dict(dataset, channel.lower(), type="molecules")

                if n_locs > 0:
                    lifetimes = self.get_lifetimes()

                    hist, bin_edges = np.histogram(lifetimes, bins=lifetime_bins, density=True)

                    self.lifetime_graph_canvas.axes.clear()

                    axes = self.lifetime_graph_canvas.axes

                    axes.hist(lifetimes, bins=lifetime_bins, label="Lifetime data", density=True, )

                    if fit_exponential:
                        def exp_decay(t, A, k):
                            return A * np.exp(-k * t)

                        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2  # Calculate bin centers
                        params, cov = curve_fit(exp_decay, bin_centers, hist, p0=[1, 0.1])

                        axes.plot(bin_centers, exp_decay(bin_centers, *params), "b--", lw=2, label=f"Fit: A={params[0]:.2f}, k={params[1]:.2f}", )

                    axes.set_xlabel("Fluorophore Lifetime (Frames)")
                    axes.set_ylabel("Probability Density")

                    axes.set_xlim(min_lifetime, max_lifetime)
                    axes.legend()

                    self.lifetime_graph_canvas.canvas.draw()

                    print("Lifetime histogram plotted")

        except:
            print(traceback.format_exc())

    def get_shapes_layer(self):
        layer_names = [layer.name for layer in self.viewer.layers]

        if "Shapes" not in layer_names:
            properties = {"mode": [], "ndim": 2}
            shapes_layer = self.viewer.add_shapes(name="Shapes", face_color="transparent",
                                                  edge_color="red", edge_width=0.1, ndim=2, properties=properties, )
        else:
            shapes_layer = self.viewer.layers["Shapes"]

        return shapes_layer

    def on_add_layer(self, event):
        if event.value.name == "Shapes":
            properties = {"mode": [], "ndim": 2}

            self.shapes_layer = self.viewer.layers["Shapes"]
            self.shapes_layer.properties = properties

            self.shapes_layer.events.data.connect(self.shapes_layer_updated)

            self.shapes_layer.current_edge_color = list(mcolors.to_rgb("green"))
            self.shapes_layer.current_face_color = [0, 0, 0, 0]
            self.shapes_layer.current_edge_width = 1
