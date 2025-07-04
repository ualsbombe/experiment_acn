#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 14:58:07 2025

@author: lau
"""

#%% THE ONE CLASS TO RULE THEM ALL

class Experiment():
    
    def __init__(self):
        pass
    
    def set_experiment_parameters(self):
        
        import numpy as np
        
        def safe_divide(a, b):
            if b == '0':
                raise ZeroDivisionError('Division by zero not allowed')
            if a % b != 0:
                raise ValueError(f"{b} is not a factor of {a}.")
            return a // b
        
        
        ## response keys
        self.target_keys_objective    = 'zm12'
        self.target_keys_subjective   = '1234'
        self.target_keys_instructions = 'zm1234'
        self.target_keys_thank_you    = ''
        self.target_keys_break        = 'c'
        
        ## refreh rate
        self.valid_refresh_rates = ['60', '120']
        
        ## breaks
        self.break_counter = 2 # initalised here for correct counting
        
        ## fixation
        self.fixation_min_frames_at_120_Hz = 60
        self.fixation_max_frames_at_120_Hz = 90
        
        ## practice
        self.practice_contrast = 0.5
        
        ## staircase 
        self.n_staircase_resets = 10
        self.n_staircase_trials = \
            safe_divide(self.experiment_info['n_experiment_trials'],
                        self.n_staircase_resets)
        self.staircase_intensity_values = np.arange(0, 1.01, 0.01)
        
        
        ## target stimuli
        self.stim_size = 200
        self.stim_frames_at_120_Hz = 50
        self.stimulus_list = ['stimulus_0', 'stimulus_0',
                              'stimulus_1', 'stimulus_1']
        
        ## mask
        self.mask_size = 200
        self.mask_frames_at_120_Hz = 4
        
        ## csv
        self.csv_header = (
                 'subject,'
                 'trial_number,'
                 'staircase_number,'
                 'fixation_duration_ms,'
                 'target_duration_ms,'
                 'target_type,'
                 'target_contrast,'
                 'mask_duration_ms,'
                 'objective_response,'
                 'objective_response_time_ms,'
                 'subjective_response,'
                 'subjective_response_time_ms'
                 '\n'
                 )
        
        ## triggers
        self.triggers = dict()
        self.triggers['stimulus_0']          = 1
        self.triggers['stimulus_1']          = 2
        self.triggers['mask']                = 3
        self.triggers['response_stimulus_0'] = 4
        self.triggers['response_stimulus_1'] = 5
        self.triggers['response_PAS1']       = 6
        self.triggers['response_PAS2']       = 7
        self.triggers['response_PAS3']       = 8
        self.triggers['response_PAS4']       = 9
        
        self.trigger_duration_s = 0.010
        
    def check_user(self):
        
        from subprocess import check_output
        from os import chdir
        from os.path import join
        
        self.user = check_output('uname -n', shell=True)
        if self.user == b'lau\n':
            self.send_triggers = True
            self.window_size = (1200, 900)
            self.fullscr = False
            self.refresh_rate = '60' ## Hz
            self.script_path = join('/home/lau/Nextcloud/arbejde/AU/',
                                    'cognitive_science/teaching/',
                                    '2025_advanced_cognitive_neuroscience/',
                                    'experiment/')
        elif self.user == b'stimpc-08\n':
            self.send_triggers = True
            self.window_size = (1200, 900)
            self.fullscr = True
            self.refresh_rate = '120' ## Hz
            self.script_path = 'please_define_me'
        else:
            raise NameError('The current user: ' + str(self.user) + \
                            ' has not been prepared')
        chdir(self.script_path)
        if self.refresh_rate not in self.valid_refresh_rates:
            raise ValueError(self.refresh_rate + ' is not among the valid' + \
                             ' refresh rates: ' + \
                                 str(self.valid_refresh_rates))
       
    def open_GUI(self):
        
        from psychopy import misc, gui, core
        from datetime import datetime
        parameter_file = 'subjective_experience.pickle'
        
        try:
            self.experiment_info = misc.fromFile(parameter_file)
        except:
            self.experiment_info = dict(subject='test',
                                        n_practice_trials=10,
                                        n_experiment_trials=400)   
            
        ## add current time
        now = datetime.now()
        self.datetime_string = now.strftime('%Y_%m_%d_%H%M%S')
        self.experiment_info['datetime'] = self.datetime_string
        
        dialgoue = gui.DlgFromDict(self.experiment_info, fixed=['datetime'])
        if dialgoue.OK:
            misc.toFile(parameter_file, self.experiment_info)
        else:
            core.quit()
    
    def define_io_files(self):
        
        from os.path import join
        
        subject = self.experiment_info['subject']
        
        prefix = join('.', 'data', f"{subject}_{self.datetime_string}_")
        
        self.practice_filename        = prefix + 'practice.csv'
        self.experiment_data_filename = prefix + 'experiment_data.csv'
    
    def define_visual_stimuli(self):
        
        from psychopy import visual
        import numpy as np
        
        self.stimulus_0 = visual.GratingStim(self.window, tex='sin',
                                             mask='gauss', sf=0.05, ori=45,
                                             size=self.stim_size)
        self.stimulus_1 = visual.GratingStim(self.window, tex='sin',
                                             mask='gauss', sf=0.05, ori=135,
                                             size=self.stim_size)
        noise_texture = np.random.rand(128, 128) * 2 - 1
        self.mask = visual.ImageStim(self.window, image=noise_texture,
                                     size=self.mask_size)
        

    def define_texts(self):
        
        self.text_dict = dict()
        self.text_dict['response_objective'] = (
             'What target stimulus was presented?\n\n'
             'Left button=Left tilt      Right button=Right tilt'
        )
        self.text_dict['response_subjective'] = (
            
            'What was the quality of your subjective experience?\n\n'
            '1: No Experience\t\t2: Weak Glimpse\t\t'
            '3: Almost Clear Experience\t\t4:Clear Experience'
            )
        self.text_dict['welcome'] = (
            'Welcome to this experiment about subjective experience\n'
            ' and respiration'
            )
        self.text_dict['practice'] = (
            'We will start with a practice session to get you used to '
            'the stimuli\n\nTheir duration on the screen is brief, '
            'so pay attention!'
            )
        self.text_dict['experiment'] = (
            'We will now start the experimental session.\n\n'
            'It will consist of '
            f'{self.n_staircase_resets} blocks with breaks in between.\n\n'
            "It's tough work, so make sure to use the breaks"
            )
        self.text_dict['break'] = (
            'BREAK!\n\n'
            f"You're now going into block {self.break_counter} out of "
            f"{self.n_staircase_resets}\n\n"
            'The experimenter will establish contact with you\n and will let '
            'you carry on when you are ready to go'
            )
        self.text_dict['thank_you'] = (
            'Thank you for participating in the experiment!\n\n'
            'Please wait - the experimenter will soon help you out.'
            )

    
    def create_experiment_window(self):
        
        from psychopy import visual
        
        self.window = visual.Window(self.window_size, fullscr=self.fullscr,
                                    units='pix')
        
        self.fixation = visual.TextStim(self.window, '+')
        self.instructions = visual.TextStim(self.window, '',
                                        wrapWidth=1e4) ## to be edited in place
    
    def present_instructions(self, instructions):
        
        from psychopy import event, core
        
        if instructions == 'response_objective':
            target_keys = self.target_keys_objective
        elif instructions == 'response_subjective':
            target_keys == self.target_keys_subjective
        elif instructions == 'break':
            target_keys = self.target_keys_break
        elif instructions == 'thank_you':
            target_keys = self.target_keys_thank_you
        else:
            target_keys = self.target_keys_instructions
        
        this_text = self.text_dict[instructions]
        self.instructions.setText(this_text)
        self.instructions.draw()
        self.window.flip()
        this_response = None
        
        while this_response is None:
            all_keys = event.waitKeys()
            for this_key in all_keys:
                if this_key in target_keys:
                    this_response = 'continue'
                elif this_key == 'q':
                    self.window.close()
                    core.quit()
            event.clearEvents('mouse')
        self.window.flip()
        
    
    def frame_correction(self, frames_at_120_Hz):
        if self.refresh_rate =='60':
            this_n_frames = frames_at_120_Hz // 2 ## itneger division
        elif self.refresh_rate == '120':
            this_n_frames = frames_at_120_Hz
        else:
            raise ValueError('This refresh rate: ' + self.refresh_rate + \
                             ', is not valid (yet)')
        return this_n_frames
    
    def present_fixation(self):
        
        from random import randint
        
        this_n_frames_min = \
            self.frame_correction(self.fixation_min_frames_at_120_Hz)
        this_n_frames_max = \
            self.frame_correction(self.fixation_max_frames_at_120_Hz)
            
        self.fixation_n_frames = randint(this_n_frames_min, this_n_frames_max)
        
        for _ in range(self.fixation_n_frames):
            self.fixation.draw()
            self.window.flip()
            
    def present_target(self, contrast):
        
        self.target_n_frames = self.frame_correction(self.stim_frames_at_120_Hz)
        
        if self.this_stimulus == 'stimulus_0':
            this_target = self.stimulus_0
        elif self.this_stimulus == 'stimulus_1':
            this_target = self.stimulus_1
            
        if self.send_triggers:
            self.send_trigger_value(self.this_stimulus)
            
        for _ in range(self.target_n_frames):
            this_target.contrast = contrast
            this_target.draw()
            self.window.flip()
        
    def present_mask(self):
    
        self.mask_n_frames = self.frame_correction(self.mask_frames_at_120_Hz)
        
        if self.send_triggers:
            self.send_trigger_value('mask')
        
        for _ in range(self.mask_n_frames):
            self.mask.draw()
            self.window.flip()
    
    def present_objective_response(self):
        
        from psychopy import event, core
        from psychopy.clock import MonotonicClock
        
        this_text = self.text_dict['response_objective']
        self.instructions.setText(this_text)
        self.instructions.draw()
        self.window.flip()
        self.objective_response = None
        clock = MonotonicClock()
        while self.objective_response is None:
            all_keys = event.waitKeys()
            for this_key in all_keys:
                if this_key == 'z' or this_key == '1':
                    self.objective_response = 'stimulus_1'
                elif this_key == 'm' or this_key == '2':
                    self.objective_response = 'stimulus_0'
                elif this_key == 'q':
                    self.window.close()
                    core.quit()
                if self.send_triggers:
                    self.send_trigger_value(
                        'response_' + self.objective_response)
                event.clearEvents('mouse')
        self.objective_response_time = clock.getTime()
        
        self.window.flip()
        
    def evaluate_objective_response(self):
        if self.objective_response == self.this_stimulus:
            self.correct = 1
        else:
            self.correct = 0
                
    def present_subjective_response(self):
        
        from psychopy import event, core
        from psychopy.clock import MonotonicClock
        
        this_text = self.text_dict['response_subjective']
        self.instructions.setText(this_text)
        self.instructions.draw()
        self.window.flip()
        self.subjective_response = None
        clock = MonotonicClock()
        
        while self.subjective_response is None:
            all_keys = event.waitKeys()
            for this_key in all_keys:
                if this_key == '1':
                    self.subjective_response = '1'
                elif this_key == '2':
                    self.subjective_response = '2'
                elif this_key == '3':
                    self.subjective_response = '3'
                elif this_key == '4':
                    self.subjective_response = '4'
                elif this_key == 'q':
                    self.window.close()
                    core.quit()
                if self.send_triggers:
                    self.send_trigger_value(
                        'response_PAS' + self.subjective_response)    
                event.clearEvents('mouse')
        self.subjective_response_time = clock.getTime()
        self.window.flip()
    
    
    def define_staircase(self):
        
        from psychopy.data import QuestHandler
        
        self.staircase = QuestHandler(0.5, 0.2,
                                      pThreshold=0.75, gamma=0.01,
                                      nTrials=self.n_staircase_trials,
                                      minVal=0.1, maxVal=1)
        
        
        ## addResponse does not work in QeuestPlus
        # self.staircase = QuestPlusHandler(
        #     nTrials=self.n_staircase_trials,
        #     intensityVals=self.staircase_intensity_values,
        #     thresholdVals=self.staircase_intensity_values,
        #     slopeVals=3.5,
        #     lowerAsymptoteVals=0.5,
        #     lapseRateVals=0.02)
        
    def update_staircase(self):
        self.staircase.addResponse(self.correct)
        
    def counterbalance_stimuli(self, n_trial):
        
        from random import shuffle
        
        modulus = n_trial % len(self.stimulus_list)
        if modulus == 0:
            shuffle(self.stimulus_list)
        self.this_stimulus = self.stimulus_list[modulus]
        

    def send_trigger_value(self, trigger_type):
        
        from triggers import setParallelData
        import threading
        
        if trigger_type not in self.triggers:
            raise ValueError(f'{trigger_type} not included in {self.triggers}')
            
        self.this_trigger = self.triggers[trigger_type]
        self.this_trigger_type = trigger_type
        threading.Timer(self.trigger_duration_s,# threading makes code carry on
                        lambda: setParallelData(self.this_trigger)).start()
        self.write_to_terminal('trigger_sent')
        
        
        
    
    def write_to_terminal(self, message_type, staircase_counter=None,
                          trial_counter=None, contrast=None):
        
        if message_type == 'refresh_rate':
                string = (
                f'The expected refresh rate is: {self.refresh_rate}'
                f'Hz. PLEASE PLEASE do check that your monitor runs at this' 
                f' refresh rate'
                )
                
        elif message_type == 'setting_path':
            string = (
                f'Setting path:  {self.script_path}'
                f'io files are saved here'
                     )
        
        elif message_type == 'staircase_reset':
            string = (
            f"Staircase reset: this is staircase reset: {staircase_counter+1} "
            f"of {self.n_staircase_resets}"
                     )

        elif message_type == 'trial_info':
            string = (
            f"--------------------------------------------------------------\n"
            f"This is trial: {trial_counter+1} out of "
            f"{self.n_staircase_trials} \nIn staircase: {staircase_counter+1}"
            f" out of {self.n_staircase_resets} \n"
            f"The contrast value of the target stimulus is: {contrast}"
                     )
        elif message_type == 'correct?':
            if self.correct:
                exchangable_word = 'correctly'
            else:
                exchangable_word = 'incorrectly'
            string = 'The participant answered ' + exchangable_word
            
        elif message_type == 'subjective_response?':
            
            PASes = ['No Experience', 'Weak Glimpse',
                     'Almost Clear Experience', 'Clear Experience']
            
            string = (
                f"The participant rated their experience as: "
                f"{PASes[int(self.subjective_response)-1]}"
                     )
            
        elif message_type == 'trigger_sent':
            string = (
                f"Trigger: {self.this_trigger} sent with description: "
                f"{self.this_trigger_type}"
                )
        else:
            raise ValueError(f"Message type: {message_type} not supported")
        print('\n' + string)
        
    def collect_csv_data(self, n_trial=None, n_staircase_reset=None,
                         contrast=None):
        
        def convert_frames_to_ms(frames, refresh_rate):
            ms = frames * (1000/refresh_rate)
            return ms
        
        self.csv_data = (
    f"{self.experiment_info['subject']},"
    f"{n_trial},"
    f"{n_staircase_reset},"
    f"{convert_frames_to_ms(self.fixation_n_frames, int(self.refresh_rate))},"
    f"{convert_frames_to_ms(self.target_n_frames, int(self.refresh_rate))},"
    f"{self.this_stimulus},"
    f"{contrast},"
    f"{convert_frames_to_ms(self.mask_n_frames, int(self.refresh_rate))},"
    f"{self.objective_response},"
    f"{self.objective_response_time},",
    f"{self.subjective_response},"
    f"{self.subjective_response_time},",
    '\n'
                        )
        
    def write_csv(self, filename):
        
        from os.path import exists
        
        if not exists(filename):
            csv_file = open(filename, mode='w') ## (over)write
            csv_file.writelines(self.csv_header)
            csv_file.close()
            
        csv_file = open(filename, mode='a') ## append
        csv_file.writelines(self.csv_data)
        csv_file.close()
     
    def run_practice(self):
        
        for n_trial in range(self.experiment_info['n_practice_trials']):
            
            self.counterbalance_stimuli(n_trial)
            self.present_fixation()
            self.present_target(contrast=self.practice_contrast)
            self.present_mask()
            self.present_objective_response()
            self.evaluate_objective_response()
            self.present_subjective_response()
    
    def run_experiment(self):
                
        for n_staircase_reset in range(self.n_staircase_resets):
            
            self.write_to_terminal('staircase_reset',
                                   staircase_counter=n_staircase_reset)
            self.define_staircase() ## reset staircase
            if n_staircase_reset > 0:
                self.define_texts() ## to update break counter
                self.present_instructions('break')
                print(self.break_counter)
                self.break_counter += 1
                
                
            for n_trial, contrast in enumerate(self.staircase):
           
                self.write_to_terminal('trial_info', trial_counter=n_trial,
                                       staircase_counter=n_staircase_reset,
                                       contrast=contrast)
                self.counterbalance_stimuli(n_trial)
                self.present_fixation()
                self.present_target(contrast)
                self.present_mask()
                self.present_objective_response()
                self.evaluate_objective_response()
                self.write_to_terminal('correct?')
                self.update_staircase()
                self.present_subjective_response()
                self.write_to_terminal('subjective_response?')
                self.collect_csv_data(n_trial=n_trial,
                                      n_staircase_reset=n_staircase_reset,
                                      contrast=contrast)
                self.write_csv(self.experiment_data_filename)
            
            

          


#%% RUN EXPERIMENT

## initalise
experiment = Experiment()    

## setting up experiment
experiment.open_GUI()
experiment.set_experiment_parameters()
experiment.check_user()
experiment.write_to_terminal('refresh_rate')
experiment.define_io_files()
experiment.write_to_terminal('setting_path')
experiment.define_texts()
experiment.create_experiment_window()
experiment.define_visual_stimuli()
experiment.present_instructions('welcome')

## practice
experiment.present_instructions('practice')
experiment.run_practice()

## experiment
experiment.set_experiment_parameters()
experiment.present_instructions('experiment')
experiment.run_experiment()

## thank you

experiment.present_instructions('thank_you')