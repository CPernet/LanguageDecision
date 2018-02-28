% function CAT_fMRI
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% initiate code and set up experiment
% requires psychophysics toolbox
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Clear Matlab/Octave window:
clc
clear all
current_path = pwd;

% load stuff here - in case Matlab complains for memory
load practice_sounds
load practice_images
load sounds
load images

% session number:
S = 0;
while S == 0
    session = input ( 'Session 1 or 2? ', 's');
    if strcmp('1',session) || strcmp('2',session)
        S = 1; break
    else
        disp('input 1 or 2'); session = [];
    end
end

% session 1 = enter session numbers:
if session == '1'
    patient_ID = input('Enter MR number:', 's');
    scan_date_1 = datestr(now);
    % session 2 = enter session numbers and load previous matlab session:
elseif session == '2'
    patient_ID = input('Enter MR number:', 's');
    [file,path]=uigetfile('*mat','select previous file');
    cd(path); load(file); cd(current_path)
    scan_date_2 = datestr(now);
end

% check for Opengl compatibility, abort otherwise:
% AssertOpenGL

%turn warnings off:
warning('off')

% Reseed the random-number generator for each experiment:
rand('state',sum(100*clock));

% Set the parameters and keys want to use:
KbName('UnifyKeyNames');
keysWanted  = [KbName('a') KbName('b') KbName('e')];
% keys: a=same=1, l=different=2, s=scanner timing pulse=3, e=escape=4 %

%Set priority level for script execution:
priorityLevel=MaxPriority('GetSecs','KbCheck','KbWait');

%open a full screen window on screen 0 (main monitor):
ScreenNumber = 2;

% Open a double buffered fullscreen window and draw a black background
% and front and back buffers:
window = Screen(ScreenNumber, 'OpenWindow');
[w,rect]=Screen('OpenWindow',ScreenNumber, 0,[]);
% Screen('Flip', w);  % Update the display to show the instruction text

%Center the Screen
xcenter = rect(3)/2;
ycenter = rect(4)/2;

%Figure out the numbers to produce white, black and black
white = WhiteIndex(window); %pixel value for white
black = BlackIndex(window); %pixel value for black
gray = ((white-black)/2)+(white/4); %gray

% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %% PRACTICE section%%%%%%%%%%
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%Instruction Screen
HideCursor; 
ListenChar(2);

Screen('FillRect', w, black); %Fill Screen with black
Screen('TextSize', w, 16); % Set text size
Screen('TextFont', w, 'Arial'); %Set font style

phrase = sprintf('Hello! \n\n\n Welcome to the task \n\n\n You will have a practice first \n\n\n (Please press the button to move on)'); %write message to subjects
DrawFormattedText(w, phrase, 'center', 'center', [255 255 255]);
Screen('Flip', w);  % Update the display to show the instruction text
KbWait([],2)


phrase = sprintf('You will see pictures and sounds \n\n\n Some will match \n\n\n  Some will be different \n\n\n (Please press the button to move on)'); %write message to subjects
DrawFormattedText(w, phrase, 'center', 'center', [255 255 255]);
Screen('Flip', w);  % Update the display to show the instruction text
KbWait([],2)


phrase = sprintf('Press the button with your THUMB if they MATCH \n\n\n Press the button with your FINGER if they are DIFFERENT \n\n\n (Please press the button to move on)'); %write message to subjects
DrawFormattedText(w, phrase, 'center', 'center', [255 255 255]);
Screen('Flip', w);  % Update the display to show the instruction text
KbWait([],2)


phrase = sprintf('Press the button when you are ready to start the practice'); %write message to subjects
DrawFormattedText(w, phrase, 'center', 'center', [255 255 255]);
Screen('Flip', w);  % Update the display to show the instruction text
KbWait([],2)


%Display sequence for practice%
if session == '1'
    practice_randomlist = randperm(16);
    start_at = 1;
    ntrials = 8;
elseif session == '2'
    practice_randomlist = data.practice_randomlist;
    start_at = 9;
    ntrials = 16;
end

Screen('FillRect', w, gray); %Fill Screen with gray
display_time = 3.8;
index = 1;
isi = [4 4 4 6 6 8 8 8];
s = randperm(8);
Isi = isi(s);
FlushEvents('keyDown');
[w, rect]=Screen('OpenWindow',ScreenNumber, 0,[],32,2);
Screen('FillRect', w, [gray gray gray]);
Screen('Flip', w);
WaitSecs(2)

for i = start_at:ntrials
    
    pic = Screen('MakeTexture',w,squeeze(practice_images(practice_randomlist(i),:,:,:)));
    Screen('DrawTexture', w, pic)
    Screen('Flip', w);
    sound(practice_sounds(practice_randomlist(i),:),44100); %output chosen sound
    onset_time = GetSecs;
    
    %loop to record which key is pressed and reaction time:
    success = 0;
    while success == 0
        pressed = 0;
        while pressed == 0
            [pressed, secs, kbData] = KbCheck;
            current_time = GetSecs - onset_time;
            if current_time >= display_time
                Screen('FillRect',w,[gray gray gray]);
                Screen('Flip',w);
                WaitSecs(Isi(index)- current_time);% get the isi
                pressed = NaN;
            
            end
        end
        
        % the subject thinks the pairing (picture+sound) is correct = same
        if kbData(keysWanted(1)) == 1
            if practice_randomlist(i) == 1 || practice_randomlist(i) == 2 || ...
                    practice_randomlist(i) == 3 || practice_randomlist(i) == 4
                perf_practice(index,1)= 1;
            else
                perf_practice(index,1)= 0;
            end
            rt_practice(index) = current_time;
            Screen('FillRect',w,[gray gray gray]);
            Screen('Flip',w);
            WaitSecs(Isi(index)- current_time);% get the isi
            success = 1;
            
            % the subject thinks the pairing is not correct = different
        elseif kbData(keysWanted(2)) == 1
            if practice_randomlist(i) ~= 1 || practice_randomlist(i) ~= 2 || ...
                    practice_randomlist(i) ~= 3 || practice_randomlist(i) ~= 4
                perf_practice(index,1)= 1;
            else
                perf_practice(index,1)= 0;
            end
            rt_practice(index) = current_time;
            Screen('FillRect',w,[gray gray gray]);
            Screen('Flip',w);
            WaitSecs(Isi(index)- current_time);% get the isi
            success = 1;
            
            % e is pressed to escape
        elseif kbData(keysWanted(3)) == 1
            FlushEvents('keyDown');
            Screen('CloseAll');
            ShowCursor;
            msgbox('test aborted!', 'end', 'help');
            return
            
            %no key is pressed
        else pressed = NaN;
            rt_practice(index) = NaN;
            perf_practice(index,1)= NaN;
        end
        
        Screen('FillRect',w,[gray gray gray]);
        Screen('Flip',w);
        current_time = GetSecs - onset_time;
        if current_time <= 4
            WaitSecs(Isi(index)- current_time);% get the isi
        end
        success = 1;
    end % closes while success == 0
    index = index+1;
end % closes for ntrials


%End of practice set screen
Screen('FillRect', w, black); %Fill Screen with black
Screen('TextSize', w, 32); % Set text size
Screen('TextFont', w, 'Arial'); %Set font style
phrase = sprintf('end of practice... \n \n\n Press a button'); %write message to subjects
DrawFormattedText(w, phrase, 'center', 'center', [255 255 255]);
Screen('Flip', w);  % Update the display to show the instruction text
KbWait([],2)

phrase = sprintf('REMEMBER: Press the button with your THUMB if they MATCH \n\n\n Press the button with your FINGER if they are DIFFERENT \n\n\n Please press a button to start'); %write message to subjects
DrawFormattedText(w, phrase, 'center', 'center', [255 255 255]);
Screen('Flip', w);  % Update the display to show the instruction text
KbWait([],2)

[w, rect]=Screen('OpenWindow',ScreenNumber, 0,[],32,2);
Screen('FillRect', w, [gray gray gray]);
Screen('Flip', w);

% add feedback on performance
ListenChar(0);
showcursor;
fprintf('there was %g non responses out of 8 \n',sum(isnan(perf_practice)));
fprintf('there was %g%% correct responses \n',nanmean(perf_practice)*100);

stop = input('continue? Y/N ','s');
if strcmp('N',stop)
    disp('expe stopped')
    return
end

% % clean up
clear practice_sounds practice_images

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%      Main part of experiment - pictures and sounds %%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% %%%%%%%%%%%%%%%%%%%%%
% %Scanner set up stuff
% %%%%%%%%%%%%%%%%%%%%%%
% TR = 2.5 sec
% number slices acquired = 30
% Total duration =300 scans (291 for stimuli + 3 at start + 6 at end)

% HideCursor;

% % declare design in advance
load design
isi = diff(design(:,1));
isi = [isi ; 0]; 

if session == '1'
    items_selection = randperm(60);
    stim_presentation1 = shuffle(items_selection(1:30)); % correct
    stim_presentation2 = shuffle(items_selection(1:30)); % phono
    stim_presentation3 = shuffle(items_selection(1:30)); % sem
    stim_presentation4 = shuffle(items_selection(1:30)); % unrelated
    index1 = 1; index2 = 1;
    index3 = 1; index4 = 1;
else
    % read stim_presentation session 1 and start at 31
    items_selection = data.items_selection;
    stim_presentation1 = shuffle(items_selection(31:60));
    stim_presentation2 = shuffle(items_selection(31:60));
    stim_presentation3 = shuffle(items_selection(31:60));
    stim_presentation4 = shuffle(items_selection(31:60));
    index1 = 1; index2 = 1;
    index3 = 1; index4 = 1;
end

[w, rect]=Screen('OpenWindow',ScreenNumber, 0,[],32,2);
Screen('FillRect', w, [gray gray gray]);
Screen('Flip', w);

condition = NaN(120,1);
onset_time = NaN(120,1);
duration = NaN(120,1);
perf = NaN(120,1);
FlushEvents('keyDown');
ListenChar(2);

% monitor scanner's pulse
% -----------------------
NS = 0;
keysWanted  = [KbName('s')];
while NS <= 3
    
    pressed = 0;
    while pressed == 0
        [pressed, secs, kbData] = KbCheck;
    end
    
    if kbData(keysWanted) == 1
        NS = NS + 1;
        fprintf('pulse %g \n',NS)
        FlushEvents('keyDown');
    end
    
    WaitSecs(1);
 end


% start expe using timing
% -----------------------
keysWanted  = [KbName('a') KbName('b') KbName('e')];
Init_time = GetSecs ;    
WaitSecs(design(1,1));

for ntrial = 1:120 % 120
    
    condition(ntrial) = design(ntrial,2);
    
    if condition(ntrial) == 1
        pic = Screen('MakeTexture',w,squeeze(images(stim_presentation1(index1),:,:,:)));
        Screen('DrawTexture', w, pic)
        Screen('Flip', w); pic_time = GetSecs;
        onset_time(ntrial) = GetSecs  - Init_time;
        sound(sounds(stim_presentation1(index1),:),44100); %output chosen sound
        index1 = index1+1;
        
    elseif condition(ntrial) == 2
        pic = Screen('MakeTexture',w,squeeze(images(stim_presentation2(index2),:,:,:)));
        Screen('DrawTexture', w, pic)
        Screen('Flip', w); pic_time = GetSecs;
        onset_time(ntrial) = GetSecs  - Init_time;
        sound(sounds(stim_presentation2(index2)+60,:),44100);
        index2 = index2+1;
        
    elseif condition(ntrial) == 3
        pic = Screen('MakeTexture',w,squeeze(images(stim_presentation3(index3),:,:,:)));
        Screen('DrawTexture', w, pic)
        Screen('Flip', w); pic_time = GetSecs;
        onset_time(ntrial) = GetSecs  - Init_time;
        sound(sounds(stim_presentation3(index3)+120,:),44100); %output chosen sound
        index3 = index3+1;
        
    elseif condition(ntrial) == 4
        pic = Screen('MakeTexture',w,squeeze(images(stim_presentation4(index4),:,:,:)));
        Screen('DrawTexture', w, pic)
        Screen('Flip', w); pic_time = GetSecs;
        onset_time(ntrial) = GetSecs - Init_time;
        sound(sounds(stim_presentation4(index4)+180,:),44100); %output chosen sound
        index4 = index4+1;
    end
        
    % until the subject answers or the pic is displayed for > 3.8 sec
    success = 0;
    while success == 0
        
        % check button press
        pressed = 0;
        while pressed == 0
            [pressed, secs, kbData] = KbCheck(-1);
            current_time = GetSecs - pic_time;
            if current_time >= display_time
                screen('fillrect',w,[gray gray gray]);
                screen('flip',w);
                answer_keys(ntrial)= NaN;
                rt(ntrial) = NaN;
                duration(ntrial) = current_time;
                perf(ntrial) = NaN;
                flushevents('keydown');
                fprintf('trial %g',ntrial)
                disp('time off: no answer')
                waitsecs(isi(ntrial)- current_time); % get the isi
                success = 1;
                pressed = 1;
            end
        end
        
       % the subject thinks the pairing is correct = same
        if kbData(keysWanted(1)) == 1
            if condition(ntrial) == 1
                perf(ntrial) = 1;
            else
                perf(ntrial) = 0;
            end
            
            answer_keys(ntrial)= 1;
            rt(ntrial) = current_time;
            duration(ntrial) = rt(ntrial);
            FlushEvents('keyDown');
            % display gray screen
            Screen('FillRect',w,[gray gray gray]);
            Screen('Flip',w);
            current_time = GetSecs - pic_time;
            fprintf('trial %g',ntrial)
            disp('subject answered')
            WaitSecs(isi(ntrial)- current_time); % get the isi
            success = 1;
            
            % the subject thinks the pairing is not correct = different
        elseif kbData(keysWanted(2)) == 1
            if condition(ntrial) ~= 1
                perf(ntrial) = 1;
            else
                perf(ntrial) = 0;
            end
            
            answer_keys(ntrial) = 0;
            rt(ntrial) = current_time;
            duration(ntrial) = rt(ntrial);
            FlushEvents('keyDown');
            % display gray screen
            Screen('FillRect',w,[gray gray gray]);
            Screen('Flip',w);
            current_time = GetSecs - pic_time;
            fprintf('trial %g',ntrial)
            disp('subject answered')
            WaitSecs(isi(ntrial)- current_time); % get the isi
            success = 1;
            
            % e is pressed to escape
        elseif kbData(keysWanted(3)) == 1
            FlushEvents('keyDown');
            Screen('CloseAll');
            ShowCursor;
            ListenChar(2)
            msgbox('test aborted!', 'end', 'help');
            return
        end
    end
end


% end of the experiment
% -----------------------
keysWanted  = [KbName('s')];
NS = 0; 
while NS <= 6
    
    % monitor scanner's pulse
    % -----------------------
    pressed = 0;
    while pressed == 0
        [pressed, secs, kbData] = KbCheck;
    end
    
    if kbData(keysWanted) == 1
        NS = NS + 1;
        fprintf('pulse %g \n',NS)
        FlushEvents('keyDown');
    end
    
    WaitSecs(1);
end

%End Screen
Screen('FillRect', w, black); %Fill Screen with black
Screen('TextSize', w, 16); % Set text size
Screen('TextFont', w, 'Arial'); %Set font style
phrase = sprintf('end of task... \n\n\n THANK YOU \n\n\n Please remain still!'); %write message to subjects
DrawFormattedText(w, phrase, 'center', 'center', [255 255 255]);
Screen('Flip', w);  % Update the display to show the instruction text
WaitSecs(3);
showcursor;
ListenChar(0)
Screen('CloseAll');

%% recording and saving of data
name = sprintf('data_%s',patient_ID);
save([name]) % save all just in case

% 1st record raw data
if session == '1'
    data.practice_randomlist = practice_randomlist;
    data.items_selection = items_selection;
    data.stim_presentation1 = stim_presentation1;
    data.stim_presentation2 = stim_presentation2;
    data.stim_presentation3 = stim_presentation3;
    data.stim_presentation4 = stim_presentation4;
     
    data.perf1 = perf;
    data.rt1 = rt;
    data.conditions1 = condition;
    data.onsets1 = onset_time;
    data.durations1 = duration;
else
    data.perf2 = perf;
    data.rt2 = rt;
    data.conditions2 = condition;
    data.onsets2 = onset_time;
    data.durations2 = duration;
end

% Analysis of Performance
perf1 = perf(condition == 1)';
perf2 = perf(condition == 2)';
perf3 = perf(condition == 3)';
perf4 = perf(condition == 4)';
perf_matrix = [perf1 perf2 perf3 perf4];
perf_per_condition = nanmean(perf_matrix,1)*100;

for position = 1:30
    item_number  =  stim_presentation1(position);
    item_position1 = position;
    item_position2 = find(stim_presentation2 == item_number);
    item_position3 = find(stim_presentation3 == item_number);
    item_position4 = find(stim_presentation4 == item_number);
    tmp(position) = nansum([perf1(item_position1) perf2(item_position2) perf3(item_position3) perf4(item_position4)]);
end

% perf matrix is the perf per condition independently of which item is
% presented - score on the other hand takes into account which items was used
% for example hammer pics = [1 0 1 1] scores 0
if session == '1'
    data.perf_matrix1 = perf_matrix;
    data.perf_per_condition1 = perf_per_condition;
    data.score1 = (tmp == 4);
elseif session == '2'
    data.perf_matrix2 = perf_matrix;
    data.perf_per_condition2 = perf_per_condition;
    data.score2 = (tmp ==4);
end

save([name], 'data') % resave just what we need


