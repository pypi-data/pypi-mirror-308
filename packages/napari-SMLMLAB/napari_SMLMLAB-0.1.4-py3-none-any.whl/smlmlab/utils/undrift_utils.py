import traceback
from smlmlab.utils.compute_utils import Worker
import traceback
import numpy as np
import scipy.ndimage
import multiprocessing
from multiprocessing import shared_memory
from functools import partial
import concurrent.futures
from picasso.postprocess import undrift as picasso_undrift
from multiprocessing import Manager
import time



def detect_dataset_drift(dat, progress_dict, index):

    dataset_dict = dat["dataset_dict"]
    segmentation = dat["segmentation"]

    try:

        loc_dict = dataset_dict["loc_dict"]
        locs = loc_dict["localisations"].copy()
        picasso_info = dataset_dict["picasso_info"]
        n_frames = picasso_info[0]["Frames"]

        len_segments = n_frames // segmentation
        n_pairs = int(len_segments * (len_segments - 1))/2

        compute_progress = {"segmentation": 0,"undrift": 0, "locs": 0}

        def total_progress():

            segmentation_progress = compute_progress["segmentation"]
            undrift_progress = compute_progress["undrift"]
            locs_progress = compute_progress["locs"]

            total_progress = int((segmentation_progress + undrift_progress + locs_progress)/3)
            progress_dict[index] = total_progress

        def segmentation_callback(progress):
            compute_progress["segmentation"] = (progress/len_segments)*100
            total_progress()

        def undrift_callback(progress):
            compute_progress["undrift"] = (progress/n_pairs)*100
            total_progress()

        def locs_callback(progress):
            compute_progress["locs"] = progress
            total_progress()

        if type(segmentation) == int:
            if n_frames > segmentation:

                drift, locs = picasso_undrift(locs,
                    picasso_info,
                    segmentation=segmentation,
                    display=False,
                    segmentation_callback=segmentation_callback,
                    rcc_callback=undrift_callback,
                    )

                dataset_dict["drift"] = drift

                render_locs = undrift_locs(locs, drift, locs_callback)

                dataset_dict["localisations"] = locs
                dataset_dict["render_locs"] = render_locs

            else:
                progress_dict[index] = 100
        else:
            progress_dict[index] = 100

    except:
        print(traceback.format_exc())
        pass

    return dataset_dict


def undrift_locs(locs, drift, callback = None):

    try:

        render_locs = {}

        frame_list = np.unique([loc.frame for loc in locs])

        n_frames = len(frame_list)
        iter = 0

        for frame in frame_list:
            frame_locs = locs[locs.frame == frame]

            frame_locs.x = frame_locs.x - drift[frame][0]
            frame_locs.y = frame_locs.y - drift[frame][1]

            render_locs[frame] = np.vstack((frame_locs.y, frame_locs.x)).T.tolist()

            iter += 1

            if callback is not None:
                progress = int((iter/n_frames)*100)
                callback(progress)

    except:
        print(traceback.format_exc())
        pass

    return render_locs




class _undrift_utils:



    def picasso_undrift_finised(self):

        try:

            self.update_ui(init=False)
            self.draw_molecules(update_vis = True)

        except:
            self.update_ui(init=False)
            print(traceback.format_exc())


    def picasso_undrift_result(self, undrift_dict):

        try:

            pass

            for dataset in undrift_dict.keys():
                channel = undrift_dict[dataset]["channel"].lower()

                if dataset in self.localisation_dict["molecules"].keys():
                    if channel in self.localisation_dict["molecules"][dataset].keys():

                        loc_dict = self.localisation_dict["molecules"][dataset][channel]

                        if "drift" in undrift_dict[dataset].keys():
                            drift = undrift_dict[dataset]["drift"]
                            loc_dict["drift"] = drift

                        if "render_locs" in undrift_dict[dataset].keys():
                            render_locs = undrift_dict[dataset]["render_locs"]
                            loc_dict["render_locs"] = render_locs

                        if "localisations" in undrift_dict[dataset].keys():
                            locs = undrift_dict[dataset]["localisations"]
                            loc_dict["localisations"] = locs

        except:
            print(traceback.format_exc())
            pass

    def undrift_localisations(self, undrift_dict, segmentation,
            progress_callback=None):

        try:
            if undrift_dict != {}:
                compute_jobs = []
                progress_dict = {}

                for dataset, dataset_dict in undrift_dict.items():
                    compute_jobs.append({"dataset": dataset, "dataset_dict": dataset_dict, "segmentation": segmentation})

                    progress_dict[dataset] = 0

                cpu_count = int(multiprocessing.cpu_count() * 0.9)

                with Manager() as manager:
                    progress_dict = manager.dict()

                    with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count) as executor:
                        # Submit all jobs
                        futures = [executor.submit(detect_dataset_drift, job, progress_dict, i) for i, job in enumerate(compute_jobs)]

                        while any(not future.done() for future in futures):
                            # Calculate and emit progress
                            total_progress = sum(progress_dict.values())
                            overall_progress = int(total_progress / len(compute_jobs))

                            if progress_callback is not None:
                                progress_callback.emit(overall_progress)

                            time.sleep(1)  # Update frequency

                        # Wait for all futures to complete
                        concurrent.futures.wait(futures)

                        # Retrieve and process results
                        results = [future.result() for future in futures]
                        for result in results:
                            if result is not None:
                                if "drift" in result.keys():

                                    drift = result["drift"]
                                    dataset = result["dataset"]
                                    locs = result["localisations"]
                                    render_locs = result["render_locs"]

                                    undrift_dict[dataset]["drift"] = drift
                                    undrift_dict[dataset]["localisations"] = locs
                                    undrift_dict[dataset]["render_locs"] = render_locs

        except:
            self.update_ui(init=False)
            print(traceback.format_exc())

        return undrift_dict

    def picasso_undrift(self, undrift_dict, segmentation, progress_callback=None):

        try:

            undrift_dict = self.undrift_localisations(undrift_dict, segmentation,
                progress_callback)

        except:
            self.update_ui(init=False)
            print(traceback.format_exc())

        return undrift_dict


    def initialise_undrift(self):

        try:
            dataset = self.gui.picasso_undrift_dataset.currentText()
            channel = self.gui.picasso_undrift_channel.currentText()
            segmentation = int(self.gui.picasso_undrift_segmentation.text())

            if dataset == "All Datasets":
                dataset_list = list(self.dataset_dict.keys())
            else:
                dataset_list = [dataset]

            undrift_dict = {}

            for dataset in dataset_list:
                loc_dict, n_locs, _ = self.get_loc_dict(dataset, channel.lower())
                if n_locs > 0 and loc_dict["fitted"] == True:
                    n_frames, height, width = self.dataset_dict[dataset][channel.lower()]["data"].shape

                    picasso_info = [{'Frames': n_frames,
                                     'Height': height,
                                     'Width': width}, {}]

                    undrift_dict[dataset] = {"loc_dict": loc_dict,
                                             "n_locs": n_locs,
                                             "picasso_info": picasso_info,
                                             "channel": channel.lower(),
                                             "dataset": dataset,
                                             }

            if undrift_dict != {}:

                self.update_ui(init=True)

                worker = Worker(self.picasso_undrift, undrift_dict=undrift_dict,
                    segmentation=segmentation)
                worker.signals.progress.connect(partial(self.pixseq_progress,
                    progress_bar=self.gui.undrift_progressbar, ))
                worker.signals.result.connect(self.picasso_undrift_result)
                worker.signals.finished.connect(self.picasso_undrift_finised)
                self.threadpool.start(worker)


        except:
            self.update_ui(init=False)
            print(traceback.format_exc())