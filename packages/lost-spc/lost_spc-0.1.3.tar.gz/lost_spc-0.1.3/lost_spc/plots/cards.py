from lost_spc.calculations import (
    calculate_control_limits,
    calculate_means,
    calculate_ranges,
    calculate_standard_deviations,
)
from lost_spc.utils import get_sample_size

from .plots import shewhart_card


class R:
    def __init__(self, data, z=3, plot_calibration_data=True, restrict_zero=True):
        sample_size = get_sample_size(data)
        self.z = z
        self.m = sample_size.m
        self.plot_calibration_data = plot_calibration_data
        self.restrict_zero = restrict_zero

    def fit(self, X):
        control_limits = calculate_control_limits(X, chart_type="R", z=self.z)
        self.UCL = control_limits["UCL"]
        self.CL = control_limits["CL"]
        self.LCL = control_limits["LCL"]
        if self.LCL < 0 and self.restrict_zero:
            self.LCL = 0
        if self.plot_calibration_data:
            self.R_i_cal = calculate_ranges(X)

    def transform(self, X):
        if self.plot_calibration_data:
            cal_samples = self.R_i_cal
        else:
            cal_samples = None
        R_i = calculate_ranges(X)
        fig = shewhart_card(
            self.UCL,
            self.CL,
            self.LCL,
            R_i,
            calibration_samples=cal_samples,
            title=r"$R$-Karte",
            ylabel=r"$R_i$",
            restrict_zero=self.restrict_zero,
        )
        return fig


class X_R:
    def __init__(self, data, z=3, plot_calibration_data=True, restrict_zero=True):
        sample_size = get_sample_size(data)
        self.z = z
        self.m = sample_size.m
        self.plot_calibration_data = plot_calibration_data
        self.restrict_zero = restrict_zero

    def fit(self, X):
        control_limits = calculate_control_limits(X, chart_type="X_R", z=self.z)
        self.UCL = control_limits["UCL"]
        self.CL = control_limits["CL"]
        self.LCL = control_limits["LCL"]
        if self.LCL < 0 and self.restrict_zero:
            self.LCL = 0
        if self.plot_calibration_data:
            self.X_mean_cal = calculate_means(X)

    def transform(self, X):
        if self.plot_calibration_data:
            cal_samples = self.X_mean_cal
        else:
            cal_samples = None
        X_mean = calculate_means(X)
        fig = shewhart_card(
            self.UCL,
            self.CL,
            self.LCL,
            X_mean,
            calibration_samples=cal_samples,
            title=r"$\bar{X}$-Karte",
            ylabel=r"$\bar{X}_i$",
            restrict_zero=self.restrict_zero,
        )
        return fig


class S:
    def __init__(self, data, z=3, plot_calibration_data=True, restrict_zero=True):
        sample_size = get_sample_size(data)
        self.z = z
        self.m = sample_size.m
        self.plot_calibration_data = plot_calibration_data
        self.restrict_zero = restrict_zero

    def fit(self, X):
        control_limits = calculate_control_limits(X, chart_type="S", z=self.z)
        self.UCL = control_limits["UCL"]
        self.CL = control_limits["CL"]
        self.LCL = control_limits["LCL"]
        if self.LCL < 0 and self.restrict_zero:
            self.LCL = 0
        if self.plot_calibration_data:
            self.S_i_cal = calculate_standard_deviations(X)

    def transform(self, X):
        if self.plot_calibration_data:
            cal_samples = self.S_i_cal
        else:
            cal_samples = None
        S_i = calculate_standard_deviations(X)
        fig = shewhart_card(
            self.UCL,
            self.CL,
            self.LCL,
            S_i,
            calibration_samples=cal_samples,
            title=r"$S$-Karte",
            ylabel=r"$S_i$",
            restrict_zero=self.restrict_zero,
        )
        return fig


class X_S:
    def __init__(self, data, z=3, plot_calibration_data=False, restrict_zero=True):
        sample_size = get_sample_size(data)
        self.z = z
        self.m = sample_size.m
        self.plot_calibration_data = plot_calibration_data
        self.restrict_zero = restrict_zero

    def fit(self, X):
        control_limits = calculate_control_limits(X, chart_type="X_S", z=self.z)
        self.UCL = control_limits["UCL"]
        self.CL = control_limits["CL"]
        self.LCL = control_limits["LCL"]
        if self.LCL < 0 and self.restrict_zero:
            self.LCL = 0
        if self.plot_calibration_data:
            self.X_mean_cal = calculate_means(X)

    def transform(self, X):
        if self.plot_calibration_data:
            cal_samples = self.X_mean_cal
        else:
            cal_samples = None
        fig = X_mean = calculate_means(X)
        shewhart_card(
            self.UCL,
            self.CL,
            self.LCL,
            X_mean,
            calibration_samples=cal_samples,
            title=r"$\bar{X}$-Karte",
            ylabel=r"$\bar{X}_i$",
            restrict_zero=self.restrict_zero,
        )
        return fig
