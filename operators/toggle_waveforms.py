import bpy
from .utils.global_settings import SequenceTypes


class ToggleWaveforms(bpy.types.Operator):
    """
    ![Demo](https://i.imgur.com/HJ5ryhv.gif)
    
    Toggle drawing of waveforms for selected strips or for all audio 
    strips if no selection is active.
    """
    bl_idname = 'power_sequencer.toggle_waveforms'
    bl_label = 'Toggle Waveforms'
    bl_description = "Toggle audio waveforms"
    bl_options = {'REGISTER', 'UNDO'}

    mode = bpy.props.EnumProperty(
        items=[('auto', 'Auto', 'Automatically toggle the waveform'),
               ('on', 'On', 'Make the waveforms visible'),
               ('off', 'Off', 'Make the waveforms invisible')],
        name="Waveform visibility",
        description="Force the waveforms' visibility with On or Off, \
            or let Blender choose automatically",
        default='auto')

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        selection = bpy.context.selected_sequences
        if not selection:
            selection = bpy.context.sequences

        sequences = [s for s in selection if s.type in SequenceTypes.SOUND]

        if not sequences:
            self.report({"ERROR_INVALID_INPUT"}, "Select at least one sound strip")
            return {'CANCELLED'}

        show_waveform = None
        if self.mode == 'auto':
            from operator import attrgetter
            show_waveform = not sorted(sequences, key=attrgetter('frame_final_start'))[0].show_waveform
        else:
            show_waveform = True if self.mode == 'on' else False

        for s in sequences:
            s.show_waveform = show_waveform
        return {'FINISHED'}
