from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad.util.Radius2Sides4n import Radius2Sides4n
from super_scad_polygon.SmoothPolygon import SmoothPolygon
from super_scad_smooth_profile.RoughFactory import RoughFactory
from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory


class SmoothCone(ScadWidget):
    """
    Widget for cones with smooth edges.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 top_radius: float | None = None,
                 top_diameter: float | None = None,
                 top_outer_radius: float | None = None,
                 top_outer_diameter: float | None = None,
                 top_inner_radius: float | None = None,
                 top_inner_diameter: float | None = None,
                 bottom_radius: float | None = None,
                 bottom_diameter: float | None = None,
                 bottom_outer_radius: float | None = None,
                 bottom_outer_diameter: float | None = None,
                 bottom_inner_radius: float | None = None,
                 bottom_inner_diameter: float | None = None,
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

        :param height: The height of the cone or cylinder.
        :param top_radius: The radius at the top of the cone.
        :param top_diameter: The diameter at the top of the cone.
        :param top_outer_radius: The radius at the top of the outer cone.
        :param top_outer_diameter: The diameter at the top of the outer cone.
        :param top_inner_radius: The radius at the top of the inner cone.
        :param top_inner_diameter: The diameter at the top of the inner cone.
        :param bottom_radius: The radius at the bottom of the cone.
        :param bottom_diameter: The diameter at the bottom of the cone.
        :param bottom_outer_radius: The radius at the bottom of the outer cone.
        :param bottom_outer_diameter: The diameter at the bottom of the outer cone.
        :param bottom_inner_radius: The radius at the bottom of the inner cone.
        :param bottom_inner_diameter: The diameter at the bottom of the inner cone.
        :param center: Whether the cylinder is centered in the z-direction.
        :param top_inner_profile: The profile factory of the smooth profile to be applied at the inner top of the cone.
        :param top_outer_profile: The profile factory of the smooth profile to be applied at the outer top of the cone.
        :param bottom_outer_profile: The profile factory of the smooth profile to be applied at the outer bottom of the
                                     cone.
        :param bottom_inner_profile: The profile factory of the smooth profile to be applied at the inner bottom of the
                                     cone.
        :param top_extend_by_eps: Whether to extend the top of the cone by eps for a clear overlap.
        :param outer_extend_by_eps: Whether to extend the outer wall of the cone by eps for a clear overlap.
        :param bottom_extend_by_eps: Whether to extend the bottom of the cone by eps for a clear overlap.
        :param inner_extend_by_eps: Whether to extend the inner wall of the cone by eps for a clear overlap.
        :param rotate_extrude_angle: Specifies the number of degrees to sweep, starting at the positive X axis. The
                                     direction of the sweep follows the Right-Hand Rule, hence a negative angle sweeps
                                     clockwise.
        :param convexity: Number of "inward" curves, i.e., expected number of path crossings of an arbitrary line
                          through the child widget.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        :param fn4n: Whether to create a cone with a multiple of 4 vertices.
        """
        ScadWidget.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_exclusive({'top_radius'},
                                     {'top_diameter'},
                                     {'top_inner_radius', 'top_outer_radius'},
                                     {'top_inner_diameter', 'top_outer_diameter'})
        admission.validate_exclusive({'bottom_radius'},
                                     {'bottom_diameter'},
                                     {'bottom_inner_radius', 'bottom_outer_radius'},
                                     {'bottom_inner_diameter', 'bottom_outer_diameter'})
        admission.validate_required({'height'},
                                    {'bottom_radius',
                                     'bottom_diameter',
                                     'bottom_outer_radius',
                                     'bottom_outer_diameter'},
                                    {'top_radius',
                                     'top_diameter',
                                     'top_outer_radius',
                                     'top_outer_diameter'},
                                    {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cone is centered along the z-as.
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_extend_by_eps(self) -> bool:
        """
        Returns whether the top of the cone is extended by eps.
        """
        return self._args.get('top_extend_by_eps', False)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_extend_by_eps(self) -> bool:
        """
        Returns whether the outer wall of the cone is extended by eps.
        """
        return self._args.get('outer_extend_by_eps', False)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_extend_by_eps(self) -> bool:
        """
        Returns whether the bottom of the cone is extended (outwards) by eps.
        """
        return self._args.get('bottom_extend_by_eps', False)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_extend_by_eps(self) -> bool:
        """
        Returns whether the inner wall of the cone is extended (inwards) by eps.
        """
        return self._args.get('inner_extend_by_eps', False)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_outer_radius(self) -> float:
        """
        Returns the top outer radius of the cone.
        """
        return self.uc(self._args.get('top_outer_radius',
                                      self._args.get('top_radius',
                                                     0.5 * self._args.get('top_outer_diameter',
                                                                          self._args.get('top_diameter', 0.0)))))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_outer_diameter(self) -> float:
        """
        Returns the top outer diameter of the cone.
        """
        return self.uc(self._args.get('top_outer_diameter',
                                      self._args.get('top_diameter',
                                                     2.0 * self._args.get('top_outer_radius',
                                                                          self._args.get('top_radius', 0.0)))))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_inner_radius(self) -> float:
        """
        Returns the top inner radius of the cone.
        """
        return self.uc(self._args.get('top_inner_radius', 0.5 * self._args.get('top_inner_diameter', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_inner_diameter(self) -> float:
        """
        Returns the top inner diameter of the cone.
        """
        return self.uc(self._args.get('top_inner_diameter', 2.0 * self._args.get('top_inner_radius', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_outer_radius(self) -> float:
        """
        Returns the bottom outer radius of the cone.
        """
        return self.uc(self._args.get('bottom_outer_radius',
                                      self._args.get('bottom_radius',
                                                     0.5 * self._args.get('bottom_outer_diameter',
                                                                          self._args.get('bottom_diameter', 0.0)))))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_outer_diameter(self) -> float:
        """
        Returns the bottom outer diameter of the cone.
        """
        return self.uc(self._args.get('bottom_outer_diameter',
                                      self._args.get('bottom_diameter',
                                                     2.0 * self._args.get('bottom_outer_radius',
                                                                          self._args.get('bottom_radius', 0.0)))))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_inner_radius(self) -> float:
        """
        Returns the bottom inner radius of the cone.
        """
        return self.uc(self._args.get('bottom_inner_radius', 0.5 * self._args.get('bottom_inner_diameter', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_inner_diameter(self) -> float:
        """
        Returns the bottom inner diameter of the cone.
        """
        return self.uc(self._args.get('bottom_inner_diameter', 2.0 * self._args.get('bottom_inner_radius', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_inner_profile(self) -> SmoothProfileFactory:
        """
        Returns the top inner profile of the cone. 
        """
        if 'top_inner_profile' in self._args:
            return self._args.get('top_inner_profile')

        return RoughFactory()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_outer_profile(self) -> SmoothProfileFactory:
        """
        Returns the top outer profile of the cone. 
        """
        if 'top_outer_profile' in self._args:
            return self._args.get('top_outer_profile')

        return RoughFactory()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_inner_profile(self) -> SmoothProfileFactory:
        """
        Returns the bottom inner profile of the cone. 
        """
        if 'bottom_inner_profile' in self._args:
            return self._args.get('bottom_inner_profile')

        return RoughFactory()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_outer_profile(self) -> SmoothProfileFactory:
        """
        Returns the bottom outer profile of the cone. 
        """
        if 'bottom_outer_profile' in self._args:
            return self._args.get('bottom_outer_profile')

        return RoughFactory()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height of the cone.
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

        if self.top_inner_radius != 0.0 and self.bottom_inner_radius != 0.0:
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
    def real_fn(self, context: Context) -> int | None:
        """
        Returns the real fixed number of fragments in 360 degrees.
        """
        if self.fn4n:
            return Radius2Sides4n.r2sides4n(context, max(self.bottom_outer_radius, self.top_outer_radius))

        return self.fn

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
        top_height = self.height / 2.0 if self.center else self.height
        bottom_height = -self.height / 2.0 if self.center else 0.0
        top_inner_radius = self.top_inner_radius
        bottom_inner_radius = self.bottom_inner_radius
        if self.inner_extend_by_eps:
            top_inner_radius = max(top_inner_radius, context.eps)
            bottom_inner_radius = max(bottom_inner_radius, context.eps)

        profile = SmoothPolygon(primary=[Vector2(top_inner_radius, top_height),
                                         Vector2(self.top_outer_radius, top_height),
                                         Vector2(self.bottom_outer_radius, bottom_height),
                                         Vector2(bottom_inner_radius, bottom_height)],
                                profile_factories=[self.top_inner_profile,
                                                   self.top_outer_profile,
                                                   self.bottom_outer_profile,
                                                   self.bottom_inner_profile],
                                extend_sides_by_eps=[self.top_extend_by_eps,
                                                     self.outer_extend_by_eps,
                                                     self.bottom_extend_by_eps,
                                                     self.inner_extend_by_eps],
                                convexity=self.convexity)

        return RotateExtrude(angle=self.rotate_extrude_angle,
                             convexity=self.convexity,
                             fa=self.fa,
                             fs=self.fs,
                             fn=self.real_fn(context),
                             child=profile)

# ----------------------------------------------------------------------------------------------------------------------
