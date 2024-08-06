'''
Music file handling

check these:
https://stackoverflow.com/questions/65856144/check-whether-a-song-has-finished-playing-in-pygame
https://stackoverflow.com/questions/65869913/how-to-get-out-of-the-while-loop-in-pygame-when-after-playing-the-music
'''
import pygame
import os, sys
pygame.mixer.init()

mixer_channel_num = 8  # default 로 8임
current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

MUSIC_FOLDER = current_dir+'/musics/'
SOUND_EFFECT = current_dir+'/sound_effects/'


# # sound effects
sound_effect_list = ['bell','confirm','dash','drink','fist','get','hard_hit','hit','item_put_down','lazer','playerdeath','sword','water', 'break' ,'block', 'blast', 'shruff', 'small_hit', 'horn_low','horn_high']
############## not needed ###############
confirm_sound = pygame.mixer.Sound(SOUND_EFFECT+"confirm.mp3")
hit_sound = pygame.mixer.Sound(SOUND_EFFECT+"hit.mp3")
get_sound = pygame.mixer.Sound(SOUND_EFFECT+"get.mp3")
sword_sound = pygame.mixer.Sound(SOUND_EFFECT+"sword.mp3")
playerdeath_sound = pygame.mixer.Sound(SOUND_EFFECT+"playerdeath.mp3")
############## not needed ###############

sound_effects = dict()
for sound in sound_effect_list:
    sound_effects[sound] = pygame.mixer.Sound(SOUND_EFFECT+sound+'.mp3')


# music은 stage와 main에서만 튼다
def music_Q(music_file,repeat = False): #현재 재생되고 있는 음악을 확인하고 음악을 틀거나 말거나 결정해야 할때 check_playing_sound = True 로 줘야 함
    global MUSIC_FOLDER
    try:
        full_path = os.path.join(MUSIC_FOLDER, '%s.mp3'%music_file)
        pygame.mixer.music.load(full_path)
    except:
        full_path = os.path.join(MUSIC_FOLDER, '%s.wav'%music_file)
        pygame.mixer.music.load(full_path)

    song_start_time = 0 # adjust start times of the songs if needed...
    pygame.mixer.music.set_volume(1) # 0.5

    # if music_file == 'BadApple':
    #     pygame.mixer.music.set_volume(1)
    #     song_start_time = 0
    if repeat:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()

    return song_start_time # returns start time! (in milliseconds)

def check_music_ended(song_start_time):
    #print(song_start_time)
    if song_start_time == -1: # not started
        return False
    # return True if music is still going. returns False if music is paused or ended.
    return not pygame.mixer.music.get_busy()




