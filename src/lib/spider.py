import numpy as np

from mplsoccer import Radar, FontManager, grid

URL = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
font = FontManager(URL)

def plot_radar_comparison(left, right, reference, player_left, league_left, team_left, year_left, player_right, league_right, team_right, year_right, figheight=8) -> None:
    
    low = [np.nanpercentile(reference[x], 5) for x in reference.columns]
    high = [np.nanpercentile(reference[x], 95) for x in reference.columns]
    lower_is_better=['D', 'D@15']
    radar = Radar(reference.columns, low, high, lower_is_better=lower_is_better, num_rings=4, ring_width=1, center_circle_radius=1)
    fig, axs = grid(figheight=figheight, grid_height=0.915, title_height=0.06, endnote_height=0.025, title_space=0, endnote_space=0, grid_key='radar', axis=False)

    # plot radar
    radar.setup_axis(ax=axs['radar'])  # format axis as a radar
    rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#f4f4f4')
    radar_output = radar.draw_radar_compare(left.values[0], right.values[0], ax=axs['radar'], kwargs_radar={'facecolor': '#e78184', 'alpha': 0.8}, kwargs_compare={'facecolor': '#769fc5', 'alpha': 0.8})
    radar_poly, radar_poly2, vertices1, vertices2 = radar_output
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=10, fontproperties=font.prop)
    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=20, fontproperties=font.prop)

    # adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
    # Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
    title1_text = axs['title'].text(0.01, 1, player_left, fontsize=30, fontproperties=font.prop, ha='left', va='center', color='#FF0000')
    title2_text = axs['title'].text(0.01, 0.2, f"{league_left} - {team_left}", fontsize=20, fontproperties=font.prop, ha='left', va='center', color='#FF0000')
    title3_text = axs['title'].text(0.01, -0.3, year_left, fontsize=20, fontproperties=font.prop, ha='left', va='center', color='#FF0000')
    title4_text = axs['title'].text(0.99, 1, player_right, fontsize=30, fontproperties=font.prop, ha='right', va='center', color='#0068C9')
    title5_text = axs['title'].text(0.99, 0.2, f"{league_right} - {team_right}", fontsize=20, fontproperties=font.prop, ha='right', va='center', color='#0068C9')
    title6_text = axs['title'].text(0.99, -0.3, year_right, fontsize=20, fontproperties=font.prop, ha='right', va='center', color='#0068C9')

    # add credits
    CREDIT_1 = "data: Riot Games"
    CREDIT_2 = "@zatfer17"

    fig.text(0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}", size=20, fontproperties=font.prop, color="#28344e", ha="right")

    return fig