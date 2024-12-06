import warnings
import inspect
import copy
import pandas as pd
import numpy as np
import os
from scipy.interpolate import griddata, RBFInterpolator
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
import pytz
from typing import Tuple, Optional, List


class InterpolationMethod:
    """ Utility class to define possible interpolation methods """
    GRIDDATA = "griddata"
    RBF_INTERPOLATOR = "RBFInterpolator"

    @staticmethod
    def get_all():
        """ Returns list of strings of all attributes """
        provided_class = InterpolationMethod().__class__
        attributes = inspect.getmembers(provided_class, lambda a: not (inspect.isroutine(a)))
        return [a[0] for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]

    @staticmethod
    def get_all_values() -> List[str]:
        """ Returns list of strings that are values of all attributes """
        return list(map(lambda x: getattr(InterpolationMethod(), x), InterpolationMethod().get_all()))


class ImageGenerator:
    """ Main class that inputs a region specification, values for points within the region, and interpolates """

    def __init__(self,
                 x_range: Tuple[float, float],
                 y_range: Tuple[float, float],
                 resolution: float,
                 source_points: Optional[List[Tuple[float, float]]] = None,
                 source_values: Optional[List[float]] = None,
                 include_boundary_points: bool = False,
                 num_points_per_boundary: int = 5,
                 interpolation_method: str = InterpolationMethod.RBF_INTERPOLATOR,
                 ) -> None:
        """
        :param x_range: tuple or 2D array of [float, float] indicating min, max of x range
        :param y_range: tuple or 2D array of [float, float] indicating min, max of y range
        :param resolution: float indicating discretisation interval size
        :param source_points: list of tuples (x, y) indicating point locations
        :param source_values: list of float values at source points (must be in same order)
        :param include_boundary_points: bool indicating whether to add boundary points, default False
        :param num_points_per_boundary: int indicating how many points to add along each image boundary, default 5
        :param interpolation_method: one of the supported interpolation methods, default 'RBFInterpolator'
        """

        # Set image dimensions and resolution
        self.x_range = x_range  # [min, max] x values
        self.y_range = y_range  # [min, max] y values
        self.resolution = resolution  # discretisation interval

        # Set source points and source values
        if source_points is not None:
            self.set_source_points(source_points)
        else:
            self.source_points = []
        if source_values is not None:
            self.set_source_values(source_values)
        else:
            self.source_values = []

        # Below are only relevant if boundary points do get generated
        self.num_points_per_boundary = num_points_per_boundary  # How many points should be generated at each boundary
        self.boundary_points = []  # list of tuples (x, y) for boundary points
        self.boundary_values = []  # list of values at boundary points (must be in same order)

        # Whether to artificially generate boundary points to ensure full region is interpolated.
        # Default False, can also be set to True later when generating fitted points or image.
        self.include_boundary_points = include_boundary_points
        self.generate_boundary_points()

        self.interpolation_method = None  # What type of interpolation method to use
        self.set_interpolation_method(interpolation_method)  # Sets local value, checks validity

        self.fitted_values = None  # 2D numpy array: values in full grid after interpolation

        self.cmap = plt.get_cmap('cividis')  # color map to use
        self.image = None  # PIL Image generated using fitted_values

    def set_source_values(self, source_values: List[float]) -> None:
        """
        Set source values.  Ensure there are as many values as there are source points.
        :param source_values: list of floats, must be in same order as self.source_points
        :return: None
        """
        # Check that there are as many values as we already have source points
        if len(source_values) != len(self.source_points):
            raise ValueError(f"There were {len(source_values)} source values provided but there are " +
                             f"{len(self.source_points)} source points, these numbers must match")

        self.source_values = source_values

    def set_source_points(self, source_points: List[Tuple[float, float]]) -> None:
        """
        Set source points.  Run some checks to ensure they're within bounds and there are no duplicates.
        :param source_points: list of tuples (x, y)
        :return: None
        """

        # Check all points in range
        for p in source_points:
            if not (self.x_range[0] <= p[0] <= self.x_range[1]):
                raise ValueError(f"Point {p} has an x value not in range {self.x_range}. " +
                                 f"Please ensure all points are within bounds when providing source points.")
            if not (self.y_range[0] <= p[1] <= self.y_range[1]):
                raise ValueError(f"Point {p} has a y value not in range {self.y_range}. " +
                                 f"Please ensure all points are within bounds when providing source points.")

        # Check no duplicates
        for i in range(len(source_points)):
            for j in range(i + 1, len(source_points)):
                # Check if two points identical
                if source_points[i] == source_points[j]:
                    raise ValueError(f"Two or more points have the same coordinates: {source_points[i]}. " +
                                     f"Please ensure there are no duplicates when providing source points.")

        # If we get here, points are ok to set
        self.source_points = source_points

    def set_boundary_values(self, boundary_values: List[float]) -> None:
        """
        Set boundary values
        :param boundary_values: list of floats, must be in same order as self.boundary_points
        :return: None
        """
        self.boundary_values = boundary_values

    def set_boundary_points(self, boundary_points: List[Tuple[float, float]]) -> None:
        """
        Set boundary points (overwrites any existing boundary points)
        @param boundary_points: list of tuple (x, y)
        @return: None
        """
        self.boundary_points = boundary_points

    def set_interpolation_method(self, interpolation_method: str) -> None:
        """
        Set interpolation method
        :param interpolation_method: Currently supports 'griddata' or 'RBFInterpolator'
        :return: None
        """
        if interpolation_method not in InterpolationMethod.get_all_values():
            warnings.warn(f"'{interpolation_method}' is not supported as an interpolation method.  \n" +
                          f"Options are: {InterpolationMethod.get_all_values()}. \n" +
                          f"Setting to {InterpolationMethod.RBF_INTERPOLATOR} for now.")
            self.interpolation_method = InterpolationMethod.RBF_INTERPOLATOR
            return

        # If we reach this point, interpolation_method is supported
        self.interpolation_method = interpolation_method

    def generate_boundary_points(self) -> None:
        """ Generate synthetic points along boundary of image """
        if not self.include_boundary_points:
            self.boundary_points = []
            self.boundary_values = []
            return

        # We only reach this point if self.include_boundary_points is True

        # First, create all points
        boundary_points = []
        boundary_x = np.linspace(self.x_range[0], self.x_range[1], num=self.num_points_per_boundary)
        boundary_y = np.linspace(self.y_range[0], self.y_range[1], num=self.num_points_per_boundary)
        # Add top and bottom edges
        for x in boundary_x:
            boundary_points.append((x, boundary_y[0]))
            boundary_points.append((x, boundary_y[-1]))
        # Add left and right edges
        for y in boundary_y:
            boundary_points.append((boundary_x[0], y))
            boundary_points.append((boundary_x[-1], y))
        self.boundary_points = boundary_points

        # Second, create all values of boundary points -- using value of nearest source point for each
        source_xy = [[p[0], p[1]] for p in self.source_points]
        boundary_x = [p[0] for p in self.boundary_points]
        boundary_y = [p[1] for p in self.boundary_points]
        self.boundary_values = list(griddata(source_xy, np.array(self.source_values),
                                             (boundary_x, boundary_y),
                                             method='nearest').ravel())

    def set_color_map(self, cmap) -> None:
        """ Set the color map """
        self.cmap = cmap

    def generate_fitted_values(self, include_boundary_points: bool = None) -> None:
        """
        Generate values for entire grid using source and optionally boundary points
        :param include_boundary_points: option to set / reset whether to include boundary points
        :return: fitted_values, 2D numpy array of values in full grid after interpolation
        """

        if len(self.source_points) == 0:
            raise BaseException("Cannot generate fitted values if there are no source points")
        all_points = self.source_points
        all_values = self.source_values

        # Change only if optional argument supplied, otherwise use previously set value
        if include_boundary_points is not None:
            self.include_boundary_points = include_boundary_points
            self.generate_boundary_points()

        # Ensure we include boundary points in interpolation (lists will be empty if we don't want to)
        all_points = all_points + self.boundary_points
        all_values = all_values + self.boundary_values

        mesh_grid = np.mgrid[
            self.x_range[0]: self.x_range[1]: self.resolution,
            self.y_range[0]: self.y_range[1]: self.resolution
        ]

        # Generate fitted values using preferred interpolation method
        if self.interpolation_method == InterpolationMethod.GRIDDATA:
            all_points_np = np.array(all_points)
            all_values_np = np.array(all_values)

            # TODO: Could allow for custom arguments to griddata in the future
            self.fitted_values = griddata(all_points_np, all_values_np, tuple(mesh_grid), method='cubic')

        elif self.interpolation_method == InterpolationMethod.RBF_INTERPOLATOR:
            # Create interpolator.  TODO: Could allow for custom arguments to RBFInterpolator in the future.
            interpolator = RBFInterpolator(all_points, all_values, kernel='linear')
            mesh_grid_flat = mesh_grid.reshape(2, -1).T
            fitted_values_flat = interpolator(mesh_grid_flat)
            self.fitted_values = fitted_values_flat.reshape(mesh_grid.shape[1], mesh_grid.shape[2])

        else:
            raise ValueError(f"Could not interpolate:  {self.interpolation_method} is not supported.  Please set "
                             f"another interpolation method.  Options are: {InterpolationMethod.get_all_values()}.")

        return self.fitted_values

    def get_fitted_values(self, refit: bool = False):
        """
        Retrieve all fitted values (full grid).  Note that if values have not been fitted, returns None.
        :param refit: boolean indicating whether to force refit of surface (even if one has already been fitted)
        :return: 2D numpy array with all fitted values
        """
        # Do we want to force refit?
        if refit:
            self.generate_fitted_values()

        return self.fitted_values

    def get_fitted_point_values(self, points: List[Tuple[float, float]], refit: bool = False) -> List[float]:
        """
        Retrieve values at each of the provided points after having fitting a surface
        @param points: array of (float, float), pairs of x, y -- specifying points to return values for
        @param refit: boolean indicating whether to force refit of surface (even if one has already been fitted)
        @return: array of float, indicating values at those points after surface fitting
        """
        if refit or (self.fitted_values is None):
            self.generate_fitted_values()

        fitted_point_values = []
        for point in points:
            # Convert to coordinates used in grid of fitted values
            x_index = int((point[0] - self.x_range[0]) / self.resolution)
            y_index = int((point[1] - self.y_range[0]) / self.resolution)
            fitted_point_values.append(self.fitted_values[x_index, y_index])

        return fitted_point_values

    # TODO:  We are currently constraining the fitted point values to match a pixel in the image.  But for
    # RBF Interpolator, this constraint is not necessary, it could in theory interpolate for any x, y that do not
    # have to match an x, y index.  Consider enabling this in the future.

    def generate_image(self,
                       include_boundary_points: bool = False,
                       flip_y: bool = True,
                       refit: bool = False,
                       interpolation_method: Optional[str] = None
                       ) -> Image:
        """
        Generate an image using existing class data and settings
        @param include_boundary_points: bool (default False), whether to include boundary points
        @param flip_y: bool (default True), whether to flip image across y-axis
        @param refit: bool (default False), whether to force refitting of values
        @param interpolation_method: InterpolationMethod (default None), can optionally be set / changed here
        @return: None
        """
        if len(self.source_points) == 0 or len(self.source_values) == 0:
            raise BaseException("Cannot generate image when there are no source points or no source values")

        # If include_boundary_points has changed, force refit
        if self.include_boundary_points != include_boundary_points:
            self.include_boundary_points = include_boundary_points
            refit = True

        if interpolation_method is not None:
            # If interpolation method has changed, force a refit of interpolation
            if self.interpolation_method != interpolation_method:
                refit = True
                self.set_interpolation_method(interpolation_method)

        # Ensure we have fitted values
        if refit or (self.fitted_values is None):
            self.generate_boundary_points()
            self.generate_fitted_values()

        grid_z_values = copy.copy(self.fitted_values)

        # If color map specified, convert to this
        if self.cmap is not None:
            grid_z_values = np.uint8([x * 255 for x in self.cmap(grid_z_values)])

        # Due to differing coordinate systems between np and PIL, must swap axes
        grid_z_values = np.swapaxes(grid_z_values, 0, 1)

        # Flip y axis?  This is common for images, where data is usually represented top to bottom
        if flip_y:
            grid_z_values = np.flip(grid_z_values, 0)

        # Set locally and return the image
        self.image = Image.fromarray(grid_z_values).convert("RGB")
        return self.image

    def save_image(self, save_path: str) -> None:
        """ Save the image at specified path """

        if self.image is None:
            raise BaseException("No image exists.  Generate image before trying to save.")

        # Ensure that the directory exists (and create it if it doesn't)
        head, tail = os.path.split(save_path)
        Path(head).mkdir(parents=True, exist_ok=True)

        # Save image
        self.image.convert('RGB').save(save_path)


def generate_image_sequence(data: pd.DataFrame,
                            image_gen: ImageGenerator,
                            time_window: Tuple[pd.Timestamp, pd.Timestamp] = None,
                            save_path: str = None,
                            filename_format: str = 'numerical'):
    """
    Generate a sequence of images using an image generator for a given dataset
    :param data: pandas dataframe having timestamps as index, and one column per time series
    :param time_window: [timestamp, timestamp] indicating interval over which to generate images
    :param image_gen: ImageGenerator object.  Source points must already be set.
    :param save_path: string, path to where images should be saved
    :param filename_format: string indicating filename format, either 'timestamp', or 'datetime'
    :return: None
    """
    # Set intervals that we should loop over
    if time_window is None:
        timestamps = data.index
    else:
        timestamps = data[time_window[0]:time_window[1]].index

    # Handle empty save path
    if save_path is None:
        save_path = "images/"

    # Maintain loop counter in case we need to save files using numerical format filenames
    loop_ix = 1
    for curr_time in timestamps:
        # Get this interval's values
        image_gen.set_source_values(list(data.loc[curr_time].values))

        # Generate image
        image_gen.generate_image(refit=True)

        # Save image
        filename_base = ""
        if filename_format == 'timestamp':
            # Use UTC
            utc_time = curr_time.astimezone(pytz.utc)
            filename_base = utc_time.strftime('%Y-%m-%d_%H-%M-%S')
        elif filename_format == 'numerical':
            filename_base = '{:08d}'.format(loop_ix)
        image_gen.save_image(f"{save_path}{filename_base}.jpg")

        loop_ix += 1


def generate_video(
        source_path: str,
        target_path: str = None,
        frame_rate: int = 30,
        output_format: str = 'mp4'):
    """
    Simple python wrapper for command line ffmpeg tool to generate a video of existing image sequence
    :param source_path: Where to find image sequence files (must have 8-digit numbered filenames, e.g. 00000001.jpg)
    :param target_path: Where to save the video, default "_video.mp4"
    :param frame_rate: int indicating framerate, default 30
    :param output_format: string indicating preferred output format.  Currently only mp4 and gif supported.
    """
    # TODO:  There may well be better video creation tools out there and consider replacing ffmpeg in the future.
    try:
        if output_format == 'mp4':
            if target_path is None:
                target_path = f"{source_path}_video.mp4"
            os.system(f"ffmpeg -r {frame_rate} -i {source_path}%08d.jpg -vcodec mpeg4 -y {target_path}")
        elif output_format == 'gif':
            if target_path is None:
                target_path = f"{source_path}_video.gif"
            os.system(f"ffmpeg -r {frame_rate} -i {source_path}%08d.jpg -f gif -y {target_path}")
    except BaseException:
        raise RuntimeError("Could not generate video, perhaps since ffmpeg is not installed.")
