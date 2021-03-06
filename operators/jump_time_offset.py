import bpy
from .utils.convert_duration_to_frames import convert_duration_to_frames


class JumpTimeOffset(bpy.types.Operator):
    """
    Move the time cursor forward or backward, using a duration in seconds.

    The equivalent tool in Blender only works with frames, meaning the jump will be different if your project's framerate is different. This tool fixes that issue.
    """
    bl_idname = 'power_sequencer.jump_time_offset'
    bl_label = 'Jump in Time'
    bl_description = "Jump forward or backward in time"
    bl_options = {'REGISTER'}

    duration = bpy.props.FloatProperty(
        name="Duration",
        description="The length of the jump in seconds (default: 1.0)",
        default=1.0,
        min=0)
    direction = bpy.props.EnumProperty(
        name="Direction",
        description="Jump direction, either forward or backward",
        items=[("forward", "Forward", "Jump forward in time"),
               ("backward", "Backward", "Jump backward in time")])

    @classmethod
    def poll(cls, context):
        return context is not None

    def execute(self, context):
        direction = 1 if self.direction == 'forward' else -1
        bpy.context.scene.frame_current += convert_duration_to_frames(self.duration) * direction
        return {'FINISHED'}
