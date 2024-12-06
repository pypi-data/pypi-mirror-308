import os
import glob
import fileseq
import pprint
import collections
from kabaret import flow
from kabaret.flow.object import _Manager
from kabaret.flow_contextual_dict import ContextualView, get_contextual_dict
import kabaret.app.resources as resources
from libreflow.baseflow.file import TrackedFolder,GenericRunAction,FileRevisionNameChoiceValue,list_digits

class ToggleMarking(flow.Action):

    _item = flow.Parent()

    def needs_dialog(self):
        return False
    
    def run(self,button):
        if button == 'Cancel':
            return

        self._item.to_mark.set(not self._item.to_mark.get())
    

class Img_Sequence(flow.Object):

    _map = flow.Parent()

    to_mark = flow.BoolParam(True).watched().ui(hidden=True)
    output_name = flow.SessionParam('')

    toggle_marking = flow.Child(ToggleMarking).ui(hidden=True)
    
    def child_value_changed(self, child_value):
        if child_value is self.to_mark:
            self.touch()

class Img_Sequence_Map(flow.DynamicMap):

    _action = flow.Parent()

    @classmethod
    def mapped_type(cls):
        return Img_Sequence

    def mapped_names(self, page_num=0, page_size=None):
        self.seq_dict = self.get_seq_dict()
        return self.seq_dict.keys()

    def columns(self):
        return ['Sequence', 'Output name']


    def _fill_row_cells(self,row,item):

        row['Sequence'] = self.seq_dict[item.name()]['display_name']
        if item.output_name.get() == '' :

            if len(self.mapped_names()) > 1 : 

                item.output_name.set(item.name())

            else : item.output_name.set(self._action._file.name())

        row['Output name'] = f'{item.output_name.get()}.mov'
    

    def _fill_row_style(self, style, item, row):

        style['Sequence_activate_oid'] = item.toggle_marking.oid()
        style['Sequence_icon'] = ('icons.gui', 'check' if item.to_mark.get() else 'check-box-empty')

        if not self.seq_dict[item.name()]['is_consecutive'] :

            style['activate_oid'] = None
            for c in self.columns():

                style[c+'_foreground-color'] = '#606060'
                style['Sequence_icon'] = ('icons.libreflow','error')
            

    def get_seq_dict(self):
        revision_name = self._action.revision.get()
        revision = self._action._file.get_revision(revision_name)

        target = revision.get_path()

        dirs = [d for d in glob.glob(target+'/**', recursive=True) if os.path.isdir(d)]

        seq_dict = collections.defaultdict(dict)
        i = 1
        for d in dirs :
            for seq in fileseq.findSequencesOnDisk(d) :
                seq_name = f'Img_sequence_{i:04}'
                i+=1
                seq_dict[seq_name]['display_name'] = seq.format()
                seq_dict[seq_name]['path'] = os.path.join(
                                                    os.path.dirname(list(seq)[0]),
                                                    f'{seq.basename()}{seq.padding()}{seq.extension()}')
                seq_dict[seq_name]['is_consecutive'] = seq.frameSet().isConsecutive()
        
        return dict(seq_dict)
    
    def _fill_ui(self,ui):
        ui['label'] = ''
        ui['expanded'] = True


class MarkImageSequence02(GenericRunAction):
    
    _folder = flow.Parent()
    _files = flow.Parent(2)
    _task = flow.Parent(3)
    
    revision = flow.Param(None, FileRevisionNameChoiceValue)
    sequence_data = flow.Param()
    
    def runner_name_and_tags(self):
        return 'MarkSequenceRunner', []
    
    def get_version(self, button):
        return None
    
    def get_run_label(self):
        return 'Generate playblast'
    
    def allow_context(self, context):
        return False
    
    def needs_dialog(self):
        return True
    
    def get_buttons(self):
        self.revision.revert_to_default()
        return ['Render', 'Cancel']
    
    def extra_argv(self):
        argv = super(MarkImageSequence02, self).extra_argv()
        
        settings = get_contextual_dict(self, 'settings')
        sequence = settings.get('sequence', None)
        
        if sequence is None:
            sequence = 0
        else:
            sequence = list_digits(sequence)[0]
        
        argv += [
            '-o', self._extra_argv['video_output'],
            '-t', resources.get('mark_sequence.fields', 'default.json'),
            '--project', settings.get('film', 'undefined'),
            '--sequence', sequence,
            '--scene', settings.get('shot', 'undefined'),
            '--version', self.revision.get(),
            '--studio', self.root().project().get_current_site().name(),
            '--file-name', self._extra_argv['file_name'],
            '--frame_rate', settings.get('frame_rate', 24.0),
            self._extra_argv['image_path']
        ]
        
        audio_path = self._extra_argv['audio_file']
        
        if audio_path is not None and os.path.exists(audio_path):
            argv += ['--audio-file', audio_path]
        
        return argv
    
    def _ensure_file_revision(self, name, extension, revision_name):
        mapped_name = name + '_' + extension
        
        if not self._files.has_mapped_name(mapped_name):
            default_files = self.root().project().get_task_manager().get_task_files(self._task.name())
            default_file = default_files.get(mapped_name)
            file = self._files.add_file(name, extension, tracked=True, default_path_format=(default_file[1] if default_file else None))
        else:
            file = self._files[mapped_name]
        
        if not file.has_revision(revision_name):
            revision = file.add_revision(revision_name)
            file.set_current_user_on_revision(revision_name)
        else:
            revision = file.get_revision(revision_name)
        
        file.file_type.set('Outputs')
        file.ensure_last_revision_oid()
        
        return revision
    
    def _get_audio_path(self):
        return None

    def mark_sequence(self, revision_name):
        # Compute playblast prefix
        seq_data = self.sequence_data.get()

        prefix = seq_data['output_name']
        
        source_revision = self._file.get_revision(revision_name)
        revision = self._ensure_file_revision(prefix, 'mov', revision_name)
        revision.comment.set(f'[{self._folder.name()} - {seq_data["display_name"]}] {source_revision.comment.get()}')
        
        # Get the path of the first image in folder
        img_path = seq_data['path']
        
        # Get original file name to print on frames
        file_name = self._folder.complete_name.get()

        self._extra_argv = {
            'image_path': img_path,
            'video_output': revision.get_path(),
            'file_name': file_name,
            'audio_file': self._get_audio_path()
        }
        
        return super(MarkImageSequence02, self).run('Render')
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        return self.mark_sequence(self.revision.get())


class MarkImageSequence01(flow.Action):
    _MANAGER_TYPE = _Manager

    ICON = ('icons.gui', 'mytasks.png')

    _file = flow.Parent()
    _map = flow.Parent(2)
    _task = flow.Parent(3)

    revision = flow.Param(None, FileRevisionNameChoiceValue).watched()
    img_sequence_list = flow.Child(Img_Sequence_Map).ui(expanded = True)

    def allow_context(self, context):
        return context

    def get_buttons(self):
        self.revision.revert_to_default()
        self.message.set("")
        return ['Mark Img Sequence','Close']

    def needs_dialog(self):
        return True
    
    def child_value_changed(self,child_value):
        if child_value is self.revision:
            self.img_sequence_list.touch()

    def mark_sequence(self,revision_name):
        return super(MarkImageSequence01, self).run('Render')

    def run(self,button):
        if button == 'Close':
            return

        seq_dict = self.img_sequence_list.get_seq_dict()
        self._file.mark_image_sequence_page2.revision.set(self.revision.get())

        i = 0
        for item in self.img_sequence_list.mapped_items():
            if item.to_mark.get() is True and seq_dict[item.name()]['is_consecutive'] is True :
                i+=1
                seq_dict[item.name()]["output_name"] = item.output_name.get()
                self._file.mark_image_sequence_page2.sequence_data.set(seq_dict[item.name()])
                self._file.mark_image_sequence_page2.mark_sequence(self.revision.get())
        if i == 0 :
            self.message.set("<font color = orange><b>You need atleast one valid sequence for marking</b></font>")
            return self.get_result(close=False)



def mark_img_sequence(parent):
    if isinstance(parent, (TrackedFolder)):
        r = flow.Child(MarkImageSequence01)
        r.name = 'dynamic_mark_sequence'
        return r

def mark_image_sequence_page2(parent):
    if isinstance(parent, (TrackedFolder)):
        r = flow.Child(MarkImageSequence02)
        r.name = 'mark_image_sequence_page2'
        r.ui(hidden=True)
        return r


def install_extensions(session):
    return {
        "mark_img_sequence": [
            mark_img_sequence,
            mark_image_sequence_page2,
        ]
    }


from . import _version
__version__ = _version.get_versions()['version']
