import bpy

class AlignAudios(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/xkBUzDj.gif)

    Attempt alignment between the selected audio strip to the active
    audio strip. The better the correlation, the better the result.

    This operator requires
    [ffmpeg](https://www.ffmpeg.org/download.html) and
    [scipy](https://www.scipy.org/install.html) to work. Audio must be
    converted to WAV data prior to analyzing, so longer strips may take
    longer to align. To mitigate this issue, analysis will be limited to
    the first 15 minutes of audio at most.
    """
    bl_idname = "power_sequencer.align_audios"
    bl_label = "Align Audios"
    bl_description = "Align two similar audios"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if scene.sequence_editor and scene.sequence_editor.active_strip:
            active = scene.sequence_editor.active_strip
            selected = bpy.context.selected_sequences

            if len(selected) == 2 and active in selected:
                selected.pop(selected.index(active))
                if selected[0].type == "SOUND" and active.type == "SOUND":
                    return True
        return False

    def execute(self, context):
        try:
            import scipy
        except ImportError:
            self.report({"ERROR"}, "Scipy must be installed to align audios")
            return {'FINISHED'}

        try:
            from .utils import is_ffmpeg_available
        except ImportError:
            self.report({"ERROR"}, "ffmpeg must be installed to align audios")
            return {'FINISHED'}

        # This import is here because it slows blender startup a little
        from .audiosync import find_offset

        scene = context.scene

        active = scene.sequence_editor.active_strip
        active_filepath = bpy.path.abspath(active.sound.filepath)

        selected = bpy.context.selected_sequences
        selected.pop(selected.index(active))

        align_strip = selected[0]
        align_strip_filepath = bpy.path.abspath(align_strip.sound.filepath)

        offset, score = find_offset(align_strip_filepath, active_filepath)

        initial_offset = active.frame_start - align_strip.frame_start

        fps = scene.render.fps / scene.render.fps_base
        frames = int(offset * fps)

        align_strip.frame_start -= (frames - initial_offset)

        self.report({"INFO"}, "Alignment score: " + str(round(score, 1)))

        return {'FINISHED'}
