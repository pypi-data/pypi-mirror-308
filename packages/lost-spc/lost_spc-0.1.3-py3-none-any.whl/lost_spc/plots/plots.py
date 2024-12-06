import matplotlib.pyplot as plt


def shewhart_card(
    UCL,
    CL,
    LCL,
    samples,
    calibration_samples=None,
    title="",
    ylabel="",
    fill_alpha=0.07,
    restrict_zero=True,
):
    """
    Plots a shewhart_card.

    restict_zero: Switch to restrict the lower control limit to 0 if it's below.
    """
    if restrict_zero:
        if LCL < 0:
            LCL = 0

    if calibration_samples is not None:
        x_min = -len(calibration_samples)
    else:
        x_min = 0

    # Draw control limits
    plt.hlines([UCL, CL, LCL], x_min, len(samples) - 1, colors=["black"], alpha=0.8)
    area_height = (UCL - CL) / 3
    plt.hlines(
        [CL + area_height, CL + 2 * area_height, CL - area_height, CL - 2 * area_height],
        x_min,
        len(samples) - 1,
        colors=["black"],
        alpha=0.3,
        linestyles="dashed",
    )

    # Add some coloring for the areas
    width = (x_min, len(samples) - 1)
    plt.fill_between(width, CL - area_height, CL + area_height, alpha=fill_alpha, color="green")
    plt.fill_between(
        width, CL + area_height, CL + 2 * area_height, alpha=fill_alpha, color="yellow"
    )
    plt.fill_between(
        width, CL - area_height, CL - 2 * area_height, alpha=fill_alpha, color="yellow"
    )
    plt.fill_between(width, CL + 2 * area_height, UCL, alpha=fill_alpha, color="red")
    plt.fill_between(width, CL - 2 * area_height, LCL, alpha=fill_alpha, color="red")

    # Plot points
    if calibration_samples is not None:
        plt.vlines(0, ymin=LCL, ymax=UCL, colors=["red"], linestyles="dotted", alpha=0.6)
        plt.plot(range(-len(calibration_samples), 0, 1), calibration_samples, "o-")
    plt.plot(range(len(samples)), samples, "o-")

    # Plot setup
    plt.title(title)
    plt.xlabel("Sample")
    plt.ylabel(ylabel)
    plt.grid()
    return plt.gcf()
