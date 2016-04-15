from .models import Player, Frame
from django.http import JsonResponse
from .bowling_func import roll1, roll2, roll3, create_player_and_frame
from .constans import FRAMES
from django.http import HttpResponseNotAllowed, Http404


def roll(request, pins=None):

    # if request.method != 'POST':
    #     return HttpResponseNotAllowed('POST allowed only')

    response = {}
    last_player = Player.objects.last()

    previuos_frame, old_frame = None, None

    if last_player is None:
        last_player, curr_frame = create_player_and_frame()
        player_frames = [curr_frame]
        num_frames = 1
    else:
        player_frames = Frame.objects.filter(
            player=last_player).order_by('-pk')
        num_frames = len(player_frames)
        if num_frames >= 3:
            curr_frame, previuos_frame, old_frame = player_frames[:3]
        elif num_frames == 2:
            curr_frame, previuos_frame = player_frames[:2]
        else:
            curr_frame = player_frames[0]

    if pins is not None:
        pins = int(pins)

    if curr_frame.roll1 is None:
        response['roll'] = 1
        pins = roll1(pins, curr_frame, previuos_frame, old_frame, num_frames)
    elif curr_frame.roll2 is None:
        response['roll'] = 2
        pins = roll2(pins, curr_frame, previuos_frame, num_frames)
    elif num_frames == FRAMES and curr_frame.roll3 is None and (
            curr_frame.strike or curr_frame.spare):
        response['roll'] = 3
        pins = roll3(pins, curr_frame, previuos_frame)
    else:
        # ten frames have been played, create new player and start new frame automatically
        response['roll'] = 1
        last_player, curr_frame = create_player_and_frame()
        player_frames = [curr_frame]
        num_frames = 1
        print(last_player)
        print(curr_frame.pk, curr_frame)
        previuos_frame, old_frame = None, None
        pins = roll1(pins, curr_frame, previuos_frame, old_frame, num_frames)

    curr_frame.save()

    scores = [frame.score for frame in player_frames if frame.score is not None]
    last_player.score = sum(scores)
    last_player.save()

    response['pins'] = pins
    response['frame_number'] = num_frames
    response['player_id'] = last_player.pk

    return JsonResponse(response)


def total_score(requset, player_id=None):
    response = {'frames': []}

    if player_id:
        try:
            player = Player.objects.get(pk=player_id)
        except Player.DoesNotExist:
            raise Http404("Player with id '%s' does not exist" % player_id)
    else:
        player = Player.objects.last()

    response['total_score'] = player.score

    frames = player.frame_set.order_by('pk').all()
    for n, frame in enumerate(frames, start=1):
        frame_dict = frame.get_dict()
        frame_dict['frame_number'] = n
        response['frames'].append(frame_dict)

    last_frame = frames.last()
    if last_frame.roll3 is not None:
        response['frames'][-1]['roll3'] = last_frame.roll3

    return JsonResponse(response, json_dumps_params={'indent': 4})


def start(requset):
    player = Player()
    player.save()
    Frame(player=player).save()
    return JsonResponse({'player_id': player.pk})
