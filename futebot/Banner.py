#[ON], maybe an ENV? turns the feature on and off, it has to be a panic button
#if not [ON], then remove {inline_banner}

from PIL import Image, ImageDraw, ImageFont #image processing library 

#Constants in (x,y) for elements placing on template
HOME_BADGE_POS = (48,73)
HOME_NAME_POS  = (16,218)
AWAY_BADGE_POS = (329, 73)
AWAY_NAME_POS  = (268,218)
TOURNAMENT_POS = (83,9)
FLEX_SPOT_POS  = (184, 121) #This container will show start time for match thread, and score for post game thread

#Constants for box sizes
TOURNAMENT_BOX  = (346,55)
TEAM_BADGE      = (136,136)
TEAM_NAME_BOX   = (228, 50)
FLEX_BOX        = (145, 73)

#Font constants
FONT        = ImageFont.load_default(36) #TODO: custom font
FONT_SCORE  = ImageFont.load_default(48)  #TODO: APPLY FONT SIZES
FONT_COLOR  = "black"

PLACEHOLDER_BADGE = "na_trave_futebot"

#generate a banner
def generate_base_match_thread_banner(home_team, away_team, tournament, start_time): 
    return _generate_banner(home_team, away_team, tournament, start_time)

def generate_match_banner_score(home_team, away_team, tournament, score_home, score_away):
    score = ' - '.join([score_home,score_away])
    return _generate_banner(home_team, away_team, tournament, score)

def _generate_banner(home_team, away_team, tournament, flex):
    from io import BytesIO
    #load assets
    banner     = Image.open("futebot/assets/template_banner.png")
    print(f"Buscando os emblemas dos times: <{home_team}> && <{away_team}>")
    home_badge = _get_team_badge(home_team)
    away_badge = _get_team_badge(away_team)

    #generate textboxes
    tournament = _generate_text_box(TOURNAMENT_BOX, tournament, FONT, FONT_COLOR)
    flex      = _generate_text_box(FLEX_BOX, flex, FONT, FONT_COLOR)
    home_name = _generate_text_box(TEAM_NAME_BOX, home_team, FONT, FONT_COLOR)
    away_name = _generate_text_box(TEAM_NAME_BOX, away_team, FONT, FONT_COLOR)

    #stitch it all up together
    banner.alpha_composite(tournament, TOURNAMENT_POS)
    banner.alpha_composite(home_badge, HOME_BADGE_POS)
    banner.alpha_composite(away_badge, AWAY_BADGE_POS)
    banner.alpha_composite(home_name, HOME_NAME_POS)
    banner.alpha_composite(away_name, AWAY_NAME_POS)
    banner.alpha_composite(flex, FLEX_SPOT_POS)
    byte_io = BytesIO()
    banner.save(byte_io, format="PNG") #converts png-image to bytes
    byte_io.seek(0)
    return byte_io

def _get_team_badge(team_name):
    try:
        i = Image.open("futebot/assets/team_badges/"+team_name+".png").convert('RGBA')
    except:
        i = Image.open("futebot/assets/team_badges/"+PLACEHOLDER_BADGE+".png").convert('RGBA')
    return i

def _generate_text_box(size, text, font, fontColor):
    W, H = size
    transparent = (0, 0, 0, 0)
    image = Image.new('RGBA', size, transparent)
    draw = ImageDraw.Draw(image)
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    draw.text(((W-w)/2, (H-h)/2), text, font=font, fill=fontColor)
    return image

