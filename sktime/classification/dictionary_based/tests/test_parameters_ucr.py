# -*- coding: utf-8 -*-
"""UCR test."""
import os
import sys
import time
from warnings import simplefilter

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy.stats import zscore

from sktime.classification.dictionary_based import WEASEL_STEROIDS

sys.path.append("../../..")

"""
Interesting!
FreezerSmallTrain
GestureMidAirD3
InlineSkate
MelbournePedestrian
PickupGestureWiimoteZ
PowerCons
SemgHandMovementCh2
SmoothSubspace
Worms
WormsTwoClass
"""


def load_from_ucr_tsv_to_dataframe_plain(full_file_path_and_name):
    """Load UCR datasets."""
    df = pd.read_csv(
        full_file_path_and_name,
        sep=r"\s+|\t+|\s+\t+|\t+\s+",
        engine="python",
        header=None,
    )
    y = df.pop(0).values
    df.columns -= 1
    return df, y


dataset_names_excerpt = [
    "ACSF1",
    "Adiac",
    "AllGestureWiimoteX",
    "AllGestureWiimoteY",
    "AllGestureWiimoteZ",
    "ArrowHead",
    "Beef",
    "BeetleFly",
    "BirdChicken",
    # 'BME',
    "Car",
    "CBF",
    # 'Chinatown',
    # 'ChlorineConcentration',
    # 'CinCECGTorso',
    "Coffee",
    # "Computers",
    # "CricketX",
    # "CricketY",
    # "CricketZ",
    # 'Crop',
    "DiatomSizeReduction",
    "DistalPhalanxOutlineAgeGroup",
    "DistalPhalanxOutlineCorrect",
    "DistalPhalanxTW",
    # 'DodgerLoopDay',
    # 'DodgerLoopGame',
    # 'DodgerLoopWeekend',
    # 'Earthquakes',
    "ECG200",
    # 'ECG5000',
    "ECGFiveDays",
    # 'ElectricDevices',
    # 'EOGHorizontalSignal',
    # 'EOGVerticalSignal',
    # 'EthanolLevel',
    "FaceAll",
    "FaceFour",
    "FacesUCR",
    # "FiftyWords",
    # 'Fish',
    # 'FordA',
    # 'FordB',
    # 'FreezerRegularTrain',
    # 'FreezerSmallTrain',
    # 'Fungi',
    # 'GestureMidAirD1',
    # 'GestureMidAirD2',
    # 'GestureMidAirD3',
    # 'GesturePebbleZ1',
    # 'GesturePebbleZ2',
    "GunPoint",
    # "GunPointAgeSpan",
    # "GunPointMaleVersusFemale",
    # "GunPointOldVersusYoung",
    # 'Ham',
    # 'HandOutlines',
    # 'Haptics',
    # 'Herring',
    # 'HouseTwenty',
    # 'InlineSkate',
    # "InsectEPGRegularTrain",
    # "InsectEPGSmallTrain",
    # "InsectWingbeatSound",
    "ItalyPowerDemand",
    # 'LargeKitchenAppliances',
    # 'Lightning2',
    # 'Lightning7',
    # 'Mallat',
    # 'Meat',
    # 'MedicalImages',
    # 'MelbournePedestrian',
    "MiddlePhalanxOutlineAgeGroup",
    "MiddlePhalanxOutlineCorrect",
    "MiddlePhalanxTW",
    # 'MixedShapesRegularTrain',
    # 'MixedShapesSmallTrain',
    # 'MoteStrain',
    # 'NonInvasiveFetalECGThorax1',
    # 'NonInvasiveFetalECGThorax2',
    "OliveOil",
    # "OSULeaf",
    # 'PhalangesOutlinesCorrect',
    # 'Phoneme',
    # 'PickupGestureWiimoteZ',
    # 'PigAirwayPressure',
    # 'PigArtPressure',
    # 'PigCVP',
    # 'PLAID',
    "Plane",
    # 'PowerCons',
    "ProximalPhalanxOutlineAgeGroup",
    "ProximalPhalanxOutlineCorrect",
    "ProximalPhalanxTW",
    # 'RefrigerationDevices',
    # 'Rock',
    # 'ScreenType',
    # 'SemgHandGenderCh2',
    # 'SemgHandMovementCh2',
    # 'SemgHandSubjectCh2',
    # 'ShakeGestureWiimoteZ',
    # 'ShapeletSim',
    # 'ShapesAll',
    # 'SmallKitchenAppliances',
    # 'SmoothSubspace',
    "SonyAIBORobotSurface1",
    "SonyAIBORobotSurface2",
    # 'StarLightCurves',
    # 'Strawberry',
    # 'SwedishLeaf',
    # 'Symbols',
    "SyntheticControl",
    # 'ToeSegmentation1',
    # 'ToeSegmentation2',
    # 'Trace',
    "TwoLeadECG",
    # 'TwoPatterns',
    # 'UMD',
    # 'UWaveGestureLibraryAll',
    # 'UWaveGestureLibraryX',
    # 'UWaveGestureLibraryY',
    # 'UWaveGestureLibraryZ',
    # 'Wafer',
    "Wine",
    # 'WordSynonyms',
    # 'Worms',
    # 'WormsTwoClass',
    # 'Yoga'
]


def get_classifiers(
    alphabet_size,
    binning_strategies,
    ensemble_size,
    feature_selection,
    max_feature_count,
    max_window,
    min_window,
    norm_options,
    use_first_differences,
    variance,
    word_lengths,
):
    """Obtain the benchmark classifiers."""
    clfs = {
        "WEASEL": WEASEL_STEROIDS(
            random_state=1379,
            binning_strategies=binning_strategies,
            variance=variance,
            ensemble_size=ensemble_size,
            max_feature_count=max_feature_count,
            min_window=min_window,
            max_window=max_window,
            alphabet_sizes=[alphabet_size],
            norm_options=norm_options,
            word_lengths=word_lengths,
            use_first_differences=use_first_differences,
            feature_selection=feature_selection,
            n_jobs=8,
        ),
        # "MiniRocket": make_pipeline(
        #    MiniRocket(random_state=1379),
        #    RidgeClassifierCV(alphas=np.logspace(-3, 3, 10), normalize=True)
        # )
    }
    return clfs


# DATA_PATH = "/Users/bzcschae/workspace/similarity/datasets/classification/"
# parallel_jobs = 1
DATA_PATH = "/vol/fob-wbib-vol2/wbi/schaefpa/sktime/datasets/UCRArchive_2018"
parallel_jobs = len(dataset_names_excerpt)

if __name__ == "__main__":

    def _parallel_fit(
        dataset_name,
        binning_strategies,
        variance,
        ensemble_size,
        max_feature_count,
        min_window,
        max_window,
        norm_options,
        word_lengths,
        use_first_differences,
        alphabet_size,
        feature_selection,
    ):
        sum_scores = {}

        # ignore all future warnings
        simplefilter(action="ignore", category=FutureWarning)

        X_train, y_train = load_from_ucr_tsv_to_dataframe_plain(
            os.path.join(DATA_PATH, dataset_name, dataset_name + "_TRAIN.tsv")
        )
        X_test, y_test = load_from_ucr_tsv_to_dataframe_plain(
            os.path.join(DATA_PATH, dataset_name, dataset_name + "_TEST.tsv")
        )

        clfs = get_classifiers(
            alphabet_size,
            binning_strategies,
            ensemble_size,
            feature_selection,
            max_feature_count,
            max_window,
            min_window,
            norm_options,
            use_first_differences,
            variance,
            word_lengths,
        )

        for name, _ in clfs.items():
            sum_scores[name] = {
                "dataset": [],
                "all_scores": [],
                "fit_time": 0.0,
                "pred_time": 0.0,
            }

        # z-norm training/test data
        X_train = zscore(X_train, axis=1)
        X_test = zscore(X_test, axis=1)
        X_train = np.reshape(np.array(X_train), (len(X_train), 1, -1))
        X_test = np.reshape(np.array(X_test), (len(X_test), 1, -1))

        print(
            f"Running Dataset={dataset_name}, "
            f"Train-Size={np.shape(X_train)}, "
            f"Test-Size={np.shape(X_test)}"
        )

        for name, clf in clfs.items():
            try:
                fit_time = time.time()
                clf.fit(X_train, y_train)
                fit_time = np.round(time.time() - fit_time, 5)

                pred_time = time.time()
                acc = clf.score(X_test, y_test)
                pred_time = np.round(time.time() - pred_time, 5)

                sum_scores[name]["dataset"].append(dataset_name)
                sum_scores[name]["all_scores"].append(acc)
                sum_scores[name]["fit_time"] += sum_scores[name]["fit_time"] + fit_time
                sum_scores[name]["pred_time"] += (
                    sum_scores[name]["pred_time"] + pred_time
                )

            except Exception as e:
                print("An exception occurred: {}".format(e))
                print("\tFailed: ", dataset_name, name)
                sum_scores[name]["dataset"].append(dataset_name)
                sum_scores[name]["all_scores"].append(0)
                sum_scores[name]["fit_time"] += sum_scores[name]["fit_time"] + 0
                sum_scores[name]["pred_time"] += sum_scores[name]["pred_time"] + 0
        # print("-----------------")

        return sum_scores

    csv_scores = []
    choose_binning_strategies = [["equi-depth", "equi-width"], ["equi-depth"]]
    variance = True
    choose_ensemble_size = [50, 75, 100]
    choose_max_features = [10_000]
    choose_min_window = [4, 8, 12]
    choose_alphabet_size = [2, 4]
    choose_max_window = [16, 20, 30, 40, 50]
    choose_norm_options = [[False], [True, False]]
    choose_word_lengths = [[4, 6, 8], [6, 8], [8]]
    choose_first_diff = [[True, False], [False]]
    choose_feature_selection = ["none"]

    for ensemble_size in choose_ensemble_size:
        for max_feature_count in choose_max_features:
            for min_window in choose_min_window:
                for max_window in choose_max_window:
                    for norm_options in choose_norm_options:
                        for word_lengths in choose_word_lengths:
                            for alphabet_size in choose_alphabet_size:
                                for use_first_differences in choose_first_diff:
                                    for binning_strategies in choose_binning_strategies:
                                        for (
                                            feature_selection
                                        ) in choose_feature_selection:
                                            parallel_res = Parallel(
                                                n_jobs=parallel_jobs,
                                                timeout=99999,
                                                batch_size=1,
                                            )(
                                                delayed(_parallel_fit)(
                                                    dataset,
                                                    binning_strategies,
                                                    True,
                                                    ensemble_size,
                                                    max_feature_count,
                                                    min_window,
                                                    max_window,
                                                    norm_options,
                                                    word_lengths,
                                                    use_first_differences,
                                                    alphabet_size,
                                                    feature_selection,
                                                )
                                                for dataset in dataset_names_excerpt
                                            )

                                            sum_scores = {}
                                            for result in parallel_res:
                                                if not sum_scores:
                                                    sum_scores = result
                                                else:
                                                    for name, data in result.items():
                                                        for key, value in data.items():
                                                            sum_scores[name][
                                                                key
                                                            ] += value

                                            print("\n\n---- Final results -----")

                                            for name, _ in sum_scores.items():
                                                print("---- Name", name, "-----")
                                                print(
                                                    binning_strategies,
                                                    variance,
                                                    ensemble_size,
                                                    max_feature_count,
                                                    min_window,
                                                    max_window,
                                                    norm_options,
                                                    word_lengths,
                                                    use_first_differences,
                                                    alphabet_size,
                                                    feature_selection,
                                                )

                                                mean_acc = np.round(
                                                    np.mean(
                                                        sum_scores[name]["all_scores"]
                                                    ),
                                                    3,
                                                )
                                                std_acc = np.round(
                                                    np.std(
                                                        sum_scores[name]["all_scores"]
                                                    ),
                                                    3,
                                                )
                                                median_acc = np.round(
                                                    np.median(
                                                        sum_scores[name]["all_scores"]
                                                    ),
                                                    3,
                                                )
                                                total_fit_time = np.round(
                                                    sum_scores[name]["fit_time"], 2
                                                )
                                                total_predict_time = np.round(
                                                    sum_scores[name]["pred_time"], 2
                                                )
                                                print("Total mean-accuracy:", mean_acc)
                                                print("Total std-accuracy:", std_acc)
                                                print(
                                                    "Total median-accuracy:", median_acc
                                                )
                                                print("Total fit_time:", total_fit_time)
                                                print(
                                                    "Total pred_time:",
                                                    total_predict_time,
                                                )
                                                print("-----------------")

                                                csv_scores.append(
                                                    (
                                                        name,
                                                        mean_acc,
                                                        std_acc,
                                                        median_acc,
                                                        total_fit_time,
                                                        total_predict_time,
                                                        binning_strategies,
                                                        variance,
                                                        ensemble_size,
                                                        max_feature_count,
                                                        min_window,
                                                        max_window,
                                                        norm_options,
                                                        word_lengths,
                                                        use_first_differences,
                                                        alphabet_size,
                                                        feature_selection,
                                                    )
                                                )

                                            pd.DataFrame.from_records(
                                                csv_scores,
                                                columns=[
                                                    "Classifier",
                                                    "mean_acc",
                                                    "std_acc",
                                                    "median_acc",
                                                    "total_fit_time",
                                                    "total_predict_time",
                                                    "binning_strategies",
                                                    "variance",
                                                    "ensemble_size",
                                                    "max_feature_count",
                                                    "min_window",
                                                    "max_window",
                                                    "norm_options",
                                                    "word_lengths",
                                                    "use_first_differences",
                                                    "alphabet_size",
                                                    "feature_selection",
                                                ],
                                            ).to_csv(
                                                "scores_weasel_all_parameters.csv",
                                                index=None,
                                            )
