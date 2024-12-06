from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad_smooth_profile.RoughFactory import RoughFactory
from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory

from super_scad_cone.SmoothCone import SmoothCone


class SmoothCylinder(ScadWidget):
    """
    Widget for cylinders with smooth edges.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 radius: float | None = None,
                 diameter: float | None = None,
                 outer_radius: float | None = None,
                 outer_diameter: float | None = None,
                 inner_radius: float | None = None,
                 inner_diameter: float | None = None,
                 center: bool = False,
                 top_inner_profile: SmoothProfileFactory | None = None,
                 top_outer_profile: SmoothProfileFactory | None = None,
                 bottom_outer_profile: SmoothProfileFactory | None = None,
                 bottom_inner_profile: SmoothProfileFactory | None = None,
                 top_extend_by_eps: bool | None = None,
                 outer_extend_by_eps: bool | None = None,
                 bottom_extend_by_eps: bool | None = None,
                 inner_extend_by_eps: bool | None = None,
                 rotate_extrude_angle: float = 360.0,
                 convexity: int | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 fn4n: bool | None = None):
        """
        Object constructor.

        :param height: The height of the cylinder.
        :param radius: The radius of the cylinder.
        :param diameter: The diameter of the cylinder.
        :param outer_radius: The outer radius of the cylinder.
        :param outer_diameter: The outer diameter at the top of the cylinder.
        :param inner_radius: The inner radius at the top of the cylinder.
        :param inner_diameter: The inner diameter at the top of the cylinder.
        :param center: Whether the cylinder is centered in the z-direction.
        :param top_inner_profile: The profile factory of the smooth profile to be applied at the inner top of the cylinder.
        :param top_outer_profile: The profile factory of the smooth profile to be applied at the outer top of the cylinder.
        :param bottom_outer_profile: The profile factory of the smooth profile to be applied at the outer bottom of the
                                     cylinder.
        :param bottom_inner_profile: The profile factory of the smooth profile to be applied at the inner bottom of the
                                     cylinder.
        :param top_extend_by_eps: Whether to extend the top of the cylinder by eps for a clear overlap.
        :param outer_extend_by_eps: Whether to extend the outer wall of the cylinder by eps for a clear overlap.
        :param bottom_extend_by_eps: Whether to extend the bottom of the cylinder by eps for a clear overlap.
        :param inner_extend_by_eps: Whether to extend the inner wall of the cylinder by eps for a clear overlap.
        :param rotate_extrude_angle: Specifies the number of degrees to sweep, starting at the positive X axis. The
                                     direction of the sweep follows the Right-Hand Rule, hence a negative angle sweeps
                                     clockwise.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          through the child widget.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a cylinder with a multiple of 4 vertices.
        """
        ScadWidget.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'radius', 'diameter'},
                                     {'inner_radius', 'outer_radius'},
                                     {'inner_diameter', 'outer_diameter'})
        admission.validate_required({'height'},
                                    {'radius',
                                     'diameter',
                                     'outer_radius',
                                     'outer_diameter'},
                                    {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cylinder is centered along the z-as.
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_extend_by_eps(self) -> bool:
        """
        Returns whether the top of the cylinder is extended by eps.
        """
        return self._args.get('top_extend_by_eps', False)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_extend_by_eps(self) -> bool:
        """
        Returns whether the outer wall of the cylinder is extended by eps.
        """
        return self._args.get('outer_extend_by_eps', False)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_extend_by_eps(self) -> bool:
        """
        Returns whether the bottom of the cylinder is extended (outwards) by eps.
        """
        return self._args.get('bottom_extend_by_eps', False)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_extend_by_eps(self) -> bool:
        """
        Returns whether the inner wall of the cylinder is extended (inwards) by eps.
        """
        return self._args.get('inner_extend_by_eps', False)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_radius(self) -> float:
        """
        Returns the top outer radius of the cylinder.
        """
        return self.uc(self._args.get('outer_radius',
                                      self._args.get('radius',
                                                     0.5 * self._args.get('outer_diameter',
                                                                          self._args.get('diameter', 0.0)))))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_diameter(self) -> float:
        """
        Returns the top outer diameter of the cylinder.
        """
        return self.uc(self._args.get('outer_diameter',
                                      self._args.get('diameter',
                                                     2.0 * self._args.get('outer_radius',
                                                                          self._args.get('radius', 0.0)))))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_radius(self) -> float:
        """
        Returns the top inner radius of the cylinder.
        """
        return self.uc(self._args.get('inner_radius', 0.5 * self._args.get('inner_diameter', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_diameter(self) -> float:
        """
        Returns the top inner diameter of the cylinder.
        """
        return self.uc(self._args.get('inner_diameter', 2.0 * self._args.get('inner_radius', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_inner_profile(self) -> SmoothProfileFactory:
        """
        Returns the top inner profile of the cylinder. 
        """
        if 'top_inner_profile' in self._args:
            return self._args.get('top_inner_profile')

        return RoughFactory()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_outer_profile(self) -> SmoothProfileFactory:
        """
        Returns the top outer profile of the cylinder. 
        """
        if 'top_outer_profile' in self._args:
            return self._args.get('top_outer_profile')

        return RoughFactory()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_inner_profile(self) -> SmoothProfileFactory:
        """
        Returns the bottom inner profile of the cylinder. 
        """
        if 'bottom_inner_profile' in self._args:
            return self._args.get('bottom_inner_profile')

        return RoughFactory()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_outer_profile(self) -> SmoothProfileFactory:
        """
        Returns the bottom outer profile of the cylinder. 
        """
        if 'bottom_outer_profile' in self._args:
            return self._args.get('bottom_outer_profile')

        return RoughFactory()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height of the cylinder.
        """
        return self.uc(self._args.get('height', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Returns the convexity.
        """
        if 'convexity' in self._args:
            return self._args['convexity']

        if self.inner_radius != 0.0:
            return 2

        return None

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._args.get('fa')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self.uc(self._args.get('fs'))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._args.get('fn')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn4n(self) -> bool | None:
        """
        Returns whether to create a circle with multiple of 4 vertices.
        """
        return self._args.get('fn4n')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def rotate_extrude_angle(self) -> float:
        """
        Returns the number of degrees to sweep, starting at the positive X axis.
        """
        return self._args['rotate_extrude_angle']

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        return SmoothCone(height=self.height,
                          top_outer_diameter=self.outer_diameter,
                          top_inner_diameter=self.inner_diameter,
                          bottom_outer_diameter=self.outer_diameter,
                          bottom_inner_diameter=self.inner_diameter,
                          center=self.center,
                          top_inner_profile=self.top_inner_profile,
                          top_outer_profile=self.top_outer_profile,
                          bottom_outer_profile=self.bottom_outer_profile,
                          bottom_inner_profile=self.bottom_inner_profile,
                          top_extend_by_eps=self.top_extend_by_eps,
                          outer_extend_by_eps=self.outer_extend_by_eps,
                          bottom_extend_by_eps=self.bottom_extend_by_eps,
                          inner_extend_by_eps=self.inner_extend_by_eps,
                          rotate_extrude_angle=self.rotate_extrude_angle,
                          convexity=self.convexity,
                          fa=self.fa,
                          fs=self.fs,
                          fn=self.fn,
                          fn4n=self.fn4n)

# ----------------------------------------------------------------------------------------------------------------------
