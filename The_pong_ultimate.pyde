# =========================================================
# GAME STATE
# =========================================================

menu = True
previous_match_screen = False

paused = False
pause_started = 0
pause_frozen_elapsed = 0
pause_state = ""

resume_countdown = False
resume_start = 0

countdown = False
countdown_start = 0

goal_announcement = False
goal_announcement_start = 0
goal_player = 0

round_countdown = False
round_countdown_start = 0

battle = False

quit_warning = False
quit_warning_start = 0
okay_pending = False

phase5_started = False
phase5_burst_start = 0

# Match result
match_over = False
winner = 0

# =========================================================
# PREVIOUS MATCH DATA
# =========================================================

# False = no data collect
previous_match_exists = False

previous_winner = None

previous_player1_score = None
previous_player2_score = None

previous_match_time = None

previous_player1_max_combo = None
previous_player2_max_combo = None

previous_player1_max_win_streak = None
previous_player2_max_win_streak = None

previous_max_phase = None

# TEST BARRIER
test_barrier = False

# =========================================================
# MATCH DATA
# =========================================================

# Score
player1_score = 0
player2_score = 0
score_limit = 5

# Combo
player1_combo = 0
player2_combo = 0

# Maximum Combo
player1_max_combo = 0
player2_max_combo = 0

#streak
player1_win_streak = 0
player2_win_streak = 0

# Maximum Win Streak
player1_max_win_streak = 0
player2_max_win_streak = 0

# Maximum Phase Reached
max_phase_reached = 1

#Round
current_round = 1

# Timer
match_timer = 0
timer_start = 0
timer_running = False

# =========================================================
# WINDOW
# =========================================================

w = 900
h = 650


# =========================================================
# FIELD
# =========================================================

field_w = 900
field_h = 500
field_top = 150
field_bottom = field_top + field_h


# =========================================================
# BALL
# =========================================================

x = field_w / 2
y = field_h / 2 + field_top
radius = 15

#use when goal
goal_x = x
goal_y = y

#use when end
end_x = x
end_y = y
# Accelerator
a = 0.25

# Velocity cap
vm = 30

# Heat
heat = 0

# =========================================================
# PADDLE
# =========================================================

paddle_w = 10
paddle_h = 150

left_x = 30
left_y = field_top + field_h / 2

right_x = field_w - 30
right_y = field_top + field_h / 2

paddle_speed = 20


# =========================================================
# PAUSE BUTTON
# =========================================================

pause_x = 35
pause_y = 30
pause_w = 50
pause_h = 30


# =========================================================
# KEY STATE
# =========================================================

w_pressed = False
s_pressed = False
up_pressed = False
down_pressed = False


# =========================================================
# SETUP
# =========================================================

def setup():
    size(w, h)
    ellipseMode(CENTER)
    rectMode(CENTER)
    stroke(255)
    strokeWeight(4)
    noFill()


# =========================================================
# FIELD
# =========================================================

def draw_field():
    stroke(255)
    noFill()

    # Outer frame
    strokeWeight(3)
    rect(field_w / 2, field_top + field_h / 2, field_w - 20, field_h - 20)

    # Inner frame
    strokeWeight(1)
    rect(field_w / 2, field_top + field_h / 2, field_w - 30, field_h - 30)

    # Center line
    strokeWeight(2)
    for y in range(field_top + 20, field_bottom - 20, 24):
        line(field_w / 2, y, field_w / 2, y + 12)


# =========================================================
# BALL / MATCH RESET
# =========================================================

def reset_ball():
    global x, y, vx, vy


    x = field_w / 2
    y = field_top + field_h / 2

    speed_start = 5
    angle = random(-PI / 4, PI / 4)

    if random(1) < 0.5:
        angle = PI - angle

    vx = speed_start * cos(angle)
    vy = speed_start * sin(angle)

def reset_paddles():
    global left_y, right_y

    left_y = field_top + field_h / 2
    right_y = field_top + field_h / 2
    
def reset_match_data():
    global player1_score, player2_score
    global player1_combo, player2_combo
    global player1_win_streak, player2_win_streak
    global player1_max_combo, player2_max_combo
    global player1_max_win_streak, player2_max_win_streak
    global current_round
    global max_phase_reached
    global phase5_started
    global phase5_stream_progress
    global phase5_stream_colors
    global phase5_stream_angles

    phase5_started = False
    phase5_stream_progress = []
    phase5_stream_colors = []
    phase5_stream_angles = []

    player1_score = 0
    player2_score = 0

    player1_combo = 0
    player2_combo = 0
    
    player1_win_streak = 0
    player2_win_streak = 0
    
    player1_max_combo = 0
    player2_max_combo = 0
    
    player1_max_win_streak = 0
    player2_max_win_streak = 0
    
    max_phase_reached = 1
    
    current_round = 1
    reset_paddles()
    reset_timer()
    
def save_previous_match():
    global previous_match_exists
    global previous_winner
    global previous_player1_score
    global previous_player2_score
    global previous_match_time
    global previous_player1_max_combo
    global previous_player2_max_combo
    global previous_player1_max_win_streak
    global previous_player2_max_win_streak
    global previous_max_phase

    previous_match_exists = True

    previous_winner = winner

    previous_player1_score = player1_score
    previous_player2_score = player2_score

    previous_match_time = get_match_time()

    previous_player1_max_combo = player1_max_combo
    previous_player2_max_combo = player2_max_combo

    previous_player1_max_win_streak = player1_max_win_streak
    previous_player2_max_win_streak = player2_max_win_streak

    previous_max_phase = max_phase_reached
    
def reset_match():
    global menu, countdown, countdown_start
    global match_over, winner
    global paused, resume_countdown
    global quit_warning, okay_pending
    global goal_announcement, round_countdown, battle

    menu = False

    countdown = True
    countdown_start = millis()

    match_over = False
    winner = 0

    reset_match_data()

    paused = False
    resume_countdown = False

    quit_warning = False
    okay_pending = False

    goal_announcement = False
    round_countdown = False
    battle = False

    reset_ball()


# =========================================================
# GAME STATE CONTROL
# =========================================================

def start_goal(player, last_x, last_y):

    global goal_announcement
    global goal_announcement_start
    global goal_player

    global battle
    global round_countdown
    global countdown

    global goal_x, goal_y
    global vx, vy, x, y

    goal_player = player

    goal_x = last_x
    goal_y = last_y

    # -----------------------------------------
    # STATE
    # -----------------------------------------

    battle = False
    countdown = False
    round_countdown = False

    goal_announcement = True
    goal_announcement_start = millis()

    # -----------------------------------------
    # FREEZE BALL
    # -----------------------------------------

    x = field_w / 2
    y = field_top + field_h / 2

    vx = 0
    vy = 0
    
def process_goal(player):
    global player1_score, player2_score
    global player1_combo, player2_combo
    global player1_win_streak, player2_win_streak
    global player1_max_win_streak, player2_max_win_streak

    # -----------------------------------------
    # PLAYER 2 SCORES
    # -----------------------------------------
    if player == 2:

        player2_score += 1

        player1_combo = 0

        player2_win_streak += 1

        if player2_win_streak > player2_max_win_streak:
            player2_max_win_streak = player2_win_streak

        player1_win_streak = 0


    # -----------------------------------------
    # PLAYER 1 SCORES
    # -----------------------------------------
    else:

        player1_score += 1
        player2_combo = 0

        player1_win_streak += 1

        if player1_win_streak > player1_max_win_streak:
            player1_max_win_streak = player1_win_streak

        player2_win_streak = 0

def handle_goal(player, last_x, last_y):

    stop_timer()

    process_goal(player)

    # -----------------------------------------
    # MATCH END
    # -----------------------------------------

    if player == 1 and player1_score >= score_limit:

        start_match_end(1, last_x, last_y)

    elif player == 2 and player2_score >= score_limit:

        start_match_end(2, last_x, last_y)

    # -----------------------------------------
    # NORMAL GOAL
    # -----------------------------------------

    else:

        start_goal(player, last_x, last_y)

def start_match_end(player, last_x, last_y):
    global match_over, winner
    global battle, vx, vy
    global end_x, end_y

    winner = player

    match_over = True
    battle = False
    
    end_x = last_x
    end_y = last_y
    
    vx = 0
    vy = 0
    stop_timer()
    save_previous_match()
        
def start_timer():
    global timer_start, timer_running

    if not timer_running:
        timer_start = millis()
        timer_running = True


def stop_timer():
    global match_timer, timer_start, timer_running

    if timer_running:
        match_timer += millis() - timer_start
        timer_running = False


def reset_timer():
    global match_timer, timer_start, timer_running

    match_timer = 0
    timer_start = 0
    timer_running = False


def get_match_time():
    if timer_running:
        return match_timer + (millis() - timer_start)

    return match_timer

# =========================================================
# HEAT METER
# =========================================================

def get_heat():
    speed = get_speed()
    
    # lock maximum heat
    if speed >= vm - 0.001:
        return 100

    heat = (speed - 5) / (30 - 5) * 100

    return constrain(heat, 0, 100)


def get_heat_phase():
    heat = get_heat()

    if heat < 25: 
        return 1

    elif heat < 50: 
        return 2

    elif heat < 75: 
        return 3

    elif heat < 100: 
        return 4

    else: 
        return 5
    
# =========================================================
# PAUSE / RESUME
# =========================================================

def get_phase_elapsed(start_time):
    global paused, pause_frozen_elapsed

    if paused:
        return pause_frozen_elapsed

    return millis() - start_time


def start_pause(state):
    global paused
    global pause_started
    global pause_frozen_elapsed
    global pause_state

    global w_pressed, s_pressed
    global up_pressed, down_pressed

    if paused:
        return

    paused = True
    pause_started = millis()
    pause_state = state
    
    stop_timer()

    # Clear key state
    w_pressed = False
    s_pressed = False
    up_pressed = False
    down_pressed = False

    if state == "countdown":
        pause_frozen_elapsed = millis() - countdown_start

    elif state == "goal":
        pause_frozen_elapsed = millis() - goal_announcement_start

    elif state == "round_countdown":
        pause_frozen_elapsed = millis() - round_countdown_start

    elif state == "battle":
        pause_frozen_elapsed = 0


def start_resume():
    global paused
    global resume_countdown
    global resume_start

    if not paused:
        return

    resume_countdown = True
    resume_start = millis()


def finish_resume():
    global paused, resume_countdown
    global countdown, goal_announcement
    global round_countdown, battle
    global countdown_start
    global goal_announcement_start
    global round_countdown_start

    if (
        pause_state == "countdown"
        or pause_state == "goal"
        or pause_state == "round_countdown"
    ):
        countdown = False
        goal_announcement = False
        round_countdown = False

        reset_ball()

        battle = True
        start_timer()

    elif pause_state == "battle":
        battle = True
        start_timer()

    paused = False
    resume_countdown = False


# =========================================================
# MAIN DRAW LOOP
# =========================================================

def draw():
    # Previous Match
    if previous_match_screen:
        draw_previous_match()
        return

    # Menu
    if menu:
        draw_menu()
        return

    # Match end
    if match_over:
        draw_match_end()
        return

    # Resume countdown
    if resume_countdown:
        if pause_state == "battle":
            draw_game()
        else:
            background(20)
            draw_field()
            draw_global_ui()
            draw_paddles()

        draw_resume_countdown()
        return

    # Normal game states
    if countdown:
        draw_countdown()

    elif goal_announcement:
        draw_goal_announcement()

    elif round_countdown:
        draw_round_countdown()

    else:
        draw_game()

    # Quit warning
    if quit_warning:
        draw_pause_overlay()

    # Normal pause
    elif paused:
        draw_pause_overlay()


# =========================================================
# GAME SCREENS
# =========================================================

def draw_menu():
    background(20)

    # Title
    fill(255)
    textAlign(CENTER, CENTER)
    textSize(48)
    text("THE PONG ULTIMATE", w / 2, 120)

    # Buttons
    draw_button("PLAY", w / 2, 270, 260, 60)
    draw_button("PREVIOUS MATCH", w / 2, 370, 260, 60)
    draw_button("EXIT", w / 2, 470, 260, 60)


def draw_countdown():
    global countdown, battle

    background(20)
    draw_field()
    draw_global_ui()
    draw_paddles()

    fill(255)
    textAlign(CENTER, CENTER)
    textSize(80)

    elapsed = get_phase_elapsed(countdown_start)

    if elapsed < 1000:
        text("3", w / 2, field_top + field_h / 2)

    elif elapsed < 2000:
        text("2", w / 2, field_top + field_h / 2)

    elif elapsed < 3000:
        text("1", w / 2, field_top + field_h / 2)

    elif elapsed < 4000:
        text("BATTLE!", w / 2, field_top + field_h / 2)

    else:
        countdown = False
        battle = True
        start_timer()

def draw_goal_announcement():
    global goal_announcement
    global round_countdown
    global round_countdown_start
    global current_round

    elapsed = get_phase_elapsed(goal_announcement_start)

    background(20)
    draw_field()
    draw_paddles()
    draw_global_ui()
        
    fill(255)
    noStroke()
    ellipse(goal_x, goal_y, radius * 2, radius * 2)
    
    fill(255)
    textAlign(CENTER, CENTER)
    textSize(60)

    if goal_player == 1:
        text("PLAYER 1 GOAL!", w / 2, field_top + field_h / 2)

    else:
        text("PLAYER 2 GOAL!", w / 2, field_top + field_h / 2)

    if elapsed >= 3000:
        goal_announcement = False
        
        current_round += 1
        reset_ball()

        round_countdown = True
        round_countdown_start = millis()


def draw_round_countdown():
    global round_countdown, battle

    elapsed = get_phase_elapsed(round_countdown_start)

    background(20)
    draw_field()
    draw_global_ui()
    draw_paddles()

    fill(255)
    textAlign(CENTER, CENTER)
    textSize(80)

    if elapsed < 1000:
        text("3", w / 2, field_top + field_h / 2)

    elif elapsed < 2000:
        text("2", w / 2, field_top + field_h / 2)

    elif elapsed < 3000:
        text("1", w / 2, field_top + field_h / 2)

    elif elapsed < 4000:
        text("BATTLE!", w / 2, field_top + field_h / 2)

    else:
        round_countdown = False
        battle = True
        start_timer()

def draw_match_end():
    background(20)
    draw_field()
    draw_paddles()
    draw_ball_at(end_x, end_y)
    draw_global_ui()
    
    rectMode(CENTER)
    fill(20)
    stroke(255)
    strokeWeight(3)
    rect(w / 2, 400, 450, 300)
    
    fill(255)
    textAlign(CENTER, CENTER)
    textSize(60)

    if winner == 1:
        text("PLAYER 1 WINS!", w / 2, 325)

    else:
        text("PLAYER 2 WINS!", w / 2, 325)

    draw_button("REPLAY", w / 2, 420, 220, 55)
    draw_button("QUIT", w / 2, 495, 220, 55)

# =========================================================
# PREVIOUS MATCH SCREEN
# =========================================================

def draw_previous_match():

    background(20)

    fill(255)
    textAlign(CENTER, CENTER)

    textSize(42)
    text("PREVIOUS MATCH", w / 2, 70)

    # Panel
    rectMode(CENTER)

    fill(20)
    stroke(255)
    strokeWeight(3)

    rect(w / 2, 350, 650, 500)

    fill(255)
    noStroke()

    textSize(24)

    # No previous match
    if not previous_match_exists:

        text("WINNER: None", w / 2, 150)
        text("SCORE: None", w / 2, 200)
        text("TIME: None", w / 2, 250)

        text("PLAYER 1 MAX COMBO: None", w / 2, 310)
        text("PLAYER 2 MAX COMBO: None", w / 2, 350)

        text("PLAYER 1 MAX WIN STREAK: None", w / 2, 410)
        text("PLAYER 2 MAX WIN STREAK: None", w / 2, 450)

        text("MAX PHASE: None", w / 2, 510)

    else:

        # Winner
        if previous_winner == 1:
            winner_text = "PLAYER 1"
        else:
            winner_text = "PLAYER 2"

        text("WINNER: " + winner_text, w / 2, 150)

        # Score
        text(
            "SCORE: "
            + str(previous_player1_score)
            + " : "
            + str(previous_player2_score),
            w / 2,
            200
        )

        # Time
        text(
            "TIME: " + format_previous_time(),
            w / 2,
            250
        )

        # Maximum Combo
        text(
            "PLAYER 1 MAX COMBO: "
            + str(previous_player1_max_combo),
            w / 2,
            310
        )

        text(
            "PLAYER 2 MAX COMBO: "
            + str(previous_player2_max_combo),
            w / 2,
            350
        )

        # Maximum Win Streak
        text(
            "PLAYER 1 MAX WIN STREAK: "
            + str(previous_player1_max_win_streak),
            w / 2,
            410
        )

        text(
            "PLAYER 2 MAX WIN STREAK: "
            + str(previous_player2_max_win_streak),
            w / 2,
            450
        )

        # Maximum Phase
        text(
            "MAX PHASE: "
            + str(previous_max_phase)
            + " - "
            + get_phase_name(previous_max_phase),
            w / 2,
            510
        )

    draw_button("BACK", w / 2, 585, 220, 55)
    
# =========================================================
# PAUSE SCREENS
# =========================================================

def draw_pause_screen():
    fill(255)
    textAlign(CENTER, CENTER)

    textSize(50)
    text("GAME PAUSED", w / 2, h / 2 - 70)

    draw_button("RESUME", w / 2, h / 2 + 20, 220, 55)

    draw_button("QUIT", w / 2, h / 2 + 90, 220, 55)


def draw_resume_countdown():
    global resume_countdown

    fill(255)
    textAlign(CENTER, CENTER)
    textSize(80)

    elapsed = millis() - resume_start

    if elapsed < 1000:
        text("3", w / 2, field_top + field_h / 2)

    elif elapsed < 2000:
        text("2", w / 2, field_top + field_h / 2)

    elif elapsed < 3000:
        text("1", w / 2, field_top + field_h / 2)

    elif elapsed < 4000:
        text("BATTLE!", w / 2, field_top + field_h / 2)

    else:
        finish_resume()


def draw_pause_overlay():
    # Dark overlay
    fill(0, 150)
    noStroke()

    rectMode(CORNER)
    rect(0, 0, w, h)

    rectMode(CENTER)

    if quit_warning:
        draw_quit_warning()

    elif paused:
        draw_pause_screen()


def draw_quit_warning():
    global quit_warning
    global okay_pending
    global paused
    global resume_countdown
    global menu

    elapsed = millis() - quit_warning_start

    # If OKAY was pressed and 3 seconds passed
    if okay_pending and elapsed >= 3000:
        reset_match_data()

        quit_warning = False
        okay_pending = False
        paused = False
        resume_countdown = False

        menu = True
        return

    fill(255)
    textAlign(CENTER, CENTER)

    # Warning
    textSize(50)
    text("WARNING!", w / 2, 180)

    textSize(22)
    text("THIS ACTION WILL MAKE YOU LOSE PROGRESS", w / 2, 250)

    text("ARE YOU SURE?", w / 2, 285)

    # Cancel button
    draw_button("CANCEL", w / 2 - 130, 400, 200, 55)

    # Okay button
    if elapsed >= 3000:
        draw_button("OKAY", w / 2 + 130, 400, 200, 55)

    else:
        # Disabled OKAY
        rectMode(CENTER)

        stroke(100)
        strokeWeight(2)
        fill(30)
        rect(w / 2 + 130, 400, 200, 55)

        fill(100)
        textSize(22)

        text("OKAY", w / 2 + 130, 400)


# =========================================================
# UI
# =========================================================

def draw_global_ui():
    draw_player_ui()
    draw_key_ui()
    draw_match_info_ui()
    draw_heat_ui()
    draw_pause_button()
    draw_fps_ui()
    
def draw_fps_ui():
    fps_x = w - pause_x
    fps_y = pause_y

    fill(255)
    textAlign(CENTER, CENTER)
    textSize(16)
    text("FPS " + str(int(frameRate)), fps_x, fps_y - 12)

    
def draw_heat_ui():
    heat = get_heat()
    phase = get_heat_phase()

    # Heat bar
    bar_x = w / 2
    bar_y = 95
    bar_w = 300
    bar_h = 18

    # Bar background
    rectMode(CENTER)
    stroke(150)
    strokeWeight(2)
    fill(30)
    rect(bar_x, bar_y, bar_w, bar_h)

    # Heat amount
    fill(255)
    noStroke()

    heat_w = bar_w * (heat / 100)
    rect(bar_x - bar_w / 2 + heat_w / 2, bar_y, heat_w, bar_h)

    # Heat percentage
    fill(255)
    textAlign(CENTER, CENTER)
    textSize(16)

    text("HEAT " + str(int(heat)) + "%", bar_x, bar_y - 18)
    
     # Phase
    if phase == 1:
        phase_name = "NORMAL"

    elif phase == 2:
        phase_name = "HEATING?"

    elif phase == 3:
        phase_name = "BURNING!"

    elif phase == 4:
        phase_name = "!OVERDRIVE!"

    else:
        phase_name = "!!!SPEED OF LIGHT!!!"

    textSize(16)

    # Phase status
    textSize(16)
    text("PHASE " + str(phase) + ": " + phase_name, bar_x, bar_y + 28)
    
# =========================================================
# PHASE EFFECT
# =========================================================

def draw_phase_background():

    heat = get_heat()

    # =====================================================
    # 0 - 25%
    # Dark -> Warm
    # =====================================================

    if heat < 25:

        t = heat / 25
        t = constrain(t, 0, 1)

        r = 20 + 25 * t
        g = 20 + 10 * t
        b = 20

    # =====================================================
    # 25 - 50%
    # Warm -> Orange
    # =====================================================

    elif heat < 50:

        t = (heat - 25) / 25
        t = constrain(t, 0, 1)

        r = 45 + 10 * t
        g = 30 - 5 * t
        b = 20 - 5 * t

    # =====================================================
    # 50 - 75%
    # Orange -> Blue
    # =====================================================

    elif heat < 75:

        t = (heat - 50) / 25
        t = constrain(t, 0, 1)

        r = 55 - 40 * t
        g = 25 + 15 * t
        b = 15 + 50 * t

    # =====================================================
    # 75 - 100%
    # Blue -> Deep Energy Blue
    # =====================================================

    elif heat >= 100:

        background(8, 3, 18)
        return

    else:

        t = (heat - 75) / 25
        t = constrain(t, 0, 1)
    
        r = 15 - 5 * t
        g = 40 + 15 * t
        b = 65 + 45 * t

    background(r, g, b)

        
# =========================================================
# PHASE 3 BURNING EFFECT
# =========================================================

def draw_phase3_field_fire(phase_heat):

    intensity = 1 + phase_heat

    # Same color as the ball
    fire_r = 255 - 255 * phase_heat
    fire_g = 120 + 135 * phase_heat
    fire_b = 255 * phase_heat

    noStroke()

    # Top / Bottom
    for i in range(8):

        x_pos = i * (w / 7)

        flame_h = random(12, 28) * intensity
        flame_w = random(8, 16)

        offset = random(-3, 3)

        fill(fire_r, fire_g, fire_b, 110)

        ellipse(x_pos + offset, field_top + flame_h / 2, flame_w, flame_h)

        ellipse(x_pos + offset, field_bottom - flame_h / 2, flame_w, flame_h)

    # Left / Right
    for i in range(6):

        y_pos = field_top + i * (field_h / 5)

        flame_w = random(12, 28) * intensity
        flame_h = random(8, 16)

        offset = random(-3, 3)

        fill(fire_r, fire_g, fire_b, 110)

        ellipse(flame_w / 2, y_pos + offset, flame_w, flame_h)

        ellipse(field_w - flame_w / 2, y_pos + offset, flame_w, flame_h)
        
# =====================================================
# PHASE 4 ENERGY FLOW
# =====================================================

phase4_stream_progress = []

phase4_stream_count = 15


def draw_phase4_energy_flow(phase_heat):

    global phase4_stream_progress

    # =================================================
    # CREATE STREAMS ONCE
    # =================================================

    if len(phase4_stream_progress) != phase4_stream_count:

        phase4_stream_progress = []

        for i in range(phase4_stream_count):

            progress = (i * 137.0 % 1000) / 1000.0

            phase4_stream_progress.append(progress)


    # =================================================
    # SPEED
    # =================================================

    flow_speed = 8 + phase_heat * 50

    stream_length = 45 + phase_heat * 130


    cx = field_w / 2
    cy = field_top + field_h / 2


    # =================================================
    # ENERGY STREAM
    # =================================================

    for i in range(phase4_stream_count):

        phase4_stream_progress[i] += flow_speed / 1000.0

        if phase4_stream_progress[i] >= 1:
            phase4_stream_progress[i] -= 1

        progress = phase4_stream_progress[i]


        # ---------------------------------------------
        # START POSITION
        # ---------------------------------------------

        side = i % 4

        if side == 0:

            sx = (i * 137) % field_w
            sy = field_top

        elif side == 1:

            sx = field_w
            sy = field_top + ((i * 83) % field_h)

        elif side == 2:

            sx = (i * 137) % field_w
            sy = field_bottom

        else:

            sx = 0
            sy = field_top + ((i * 83) % field_h)


        # ---------------------------------------------
        # DIRECTION → CENTER
        # ---------------------------------------------

        dx = cx - sx
        dy = cy - sy

        distance = sqrt(dx * dx + dy * dy)

        if distance == 0:
            continue

        dx /= distance
        dy /= distance


        # ---------------------------------------------
        # POSITION
        # ---------------------------------------------

        travel = progress * distance

        px = sx + dx * travel
        py = sy + dy * travel


        # ---------------------------------------------
        # TRAIL
        # ---------------------------------------------

        tail_x = px - dx * stream_length
        tail_y = py - dy * stream_length


        # ---------------------------------------------
        # FADE
        # ---------------------------------------------

        fade_start = constrain(progress * 8, 0, 1)
        fade_end = constrain((1 - progress) * 8, 0, 1)

        alpha = ((90 + phase_heat * 150) * fade_start * fade_end)


        # ---------------------------------------------
        # OUTER ENERGY
        # ---------------------------------------------

        stroke(80, 190, 255, alpha * 0.45)

        strokeWeight(3.0 + phase_heat * 3.0)

        line(tail_x, tail_y, px, py)


        # ---------------------------------------------
        # MAIN ENERGY
        # ---------------------------------------------

        stroke(180, 235, 255, alpha)

        strokeWeight(1.5 + phase_heat * 2.5)

        line(tail_x, tail_y, px, py)


    # =================================================
    # GLOWING FRAME
    # =================================================

    pulse = (sin(millis() * 0.015) + 1) / 2

    intensity = 70 + pulse * 100


    # ---------------------------------------------
    # OUTER GLOW
    # ---------------------------------------------

    noFill()

    for i in range(5):

        glow_alpha = intensity * (1 - i / 5.0)

        stroke(80, 190 + 40 * phase_heat, 255, glow_alpha)

        strokeWeight(3 + i * 3 + phase_heat * 3)

        rect(field_w / 2, field_top + field_h / 2,
            field_w - 20 + i * 4, field_h - 20 + i * 4)


    # ---------------------------------------------
    # BRIGHT FRAME CORE
    # ---------------------------------------------

    pulse_alpha = 150 + pulse * 105

    stroke(180, 235, 255, pulse_alpha)
    
    strokeWeight(2 + phase_heat * 2)

    rect(field_w / 2, field_top + field_h / 2, field_w - 20, field_h - 20)
  
# =====================================================
# PHASE 5 COSMIC RADIATION
# OUTWARD ENERGY EXPLOSION
# =====================================================

phase5_stream_progress = []
phase5_stream_colors = []
phase5_stream_angles = []

phase5_stream_count = 15
    
def create_phase5_energy():

    global phase5_stream_progress
    global phase5_stream_colors
    global phase5_stream_angles

    phase5_stream_progress = []
    phase5_stream_colors = []
    phase5_stream_angles = []

    for i in range(phase5_stream_count):

        # ---------------------------------------------
        # RANDOM START
        # ---------------------------------------------

        progress = random(0, 1)
        phase5_stream_progress.append(progress)

        # ---------------------------------------------
        # RANDOM DIRECTION
        # ---------------------------------------------

        phase5_stream_angles.append(random(TWO_PI))

        # ---------------------------------------------
        # RANDOM COLOR
        # ---------------------------------------------

        color_type = int(random(8))

        if color_type == 0:
            c = [255, 70, 70]

        elif color_type == 1:
            c = [255, 140, 40]

        elif color_type == 2:
            c = [255, 220, 70]

        elif color_type == 3:
            c = [70, 180, 255]

        elif color_type == 4:
            c = [80, 255, 220]

        elif color_type == 5:
            c = [130, 90, 255]

        elif color_type == 6:
            c = [220, 80, 255]

        else:
            c = [255, 255, 255]

        phase5_stream_colors.append(c)

def draw_phase5_cosmic_radiation():

    global phase5_stream_progress

    # Create streams once
    if len(phase5_stream_progress) != phase5_stream_count:
        create_phase5_energy()

    # =================================================
    # CENTER
    # =================================================

    cx = field_w / 2
    cy = field_top + field_h / 2

    # =================================================
    # SPEED
    # =================================================

    flow_speed = 50

    # =================================================
    # STREAM
    # =================================================

    for i in range(phase5_stream_count):

        # ---------------------------------------------
        # MOVE
        # ---------------------------------------------

        phase5_stream_progress[i] += flow_speed / 1000.0

        # ---------------------------------------------
        # RESET
        # ---------------------------------------------

        if phase5_stream_progress[i] >= 1:

            phase5_stream_progress[i] = random(0, 0.15)

            # change direction every time
            phase5_stream_angles[i] = random(TWO_PI)

            # change color every time
            color_type = int(random(8))

            if color_type == 0:
                phase5_stream_colors[i] = [255, 70, 70]

            elif color_type == 1:
                phase5_stream_colors[i] = [255, 140, 40]

            elif color_type == 2:
                phase5_stream_colors[i] = [255, 220, 70]

            elif color_type == 3:
                phase5_stream_colors[i] = [70, 180, 255]

            elif color_type == 4:
                phase5_stream_colors[i] = [80, 255, 220]

            elif color_type == 5:
                phase5_stream_colors[i] = [130, 90, 255]

            elif color_type == 6:
                phase5_stream_colors[i] = [220, 80, 255]

            else:
                phase5_stream_colors[i] = [255, 255, 255]


        progress = phase5_stream_progress[i]

        # =================================================
        # RANDOM DIRECTION
        # =================================================

        angle = phase5_stream_angles[i]

        dx = cos(angle)
        dy = sin(angle)

        # =================================================
        # FIND DISTANCE TO FIELD EDGE
        # =================================================

        distances = []

        # Right
        if dx > 0:
            distances.append((field_w - cx) / dx)

        # Left
        elif dx < 0:
            distances.append((0 - cx) / dx)

        # Bottom
        if dy > 0:
            distances.append((field_bottom - cy) / dy)

        # Top
        elif dy < 0:
            distances.append((field_top - cy) / dy)

        # pick range edge
        distances = [d for d in distances if d > 0]

        if len(distances) == 0:
            continue

        max_distance = min(distances)

        # =================================================
        # POSITION
        # =================================================

        travel = progress * max_distance

        px = cx + dx * travel
        py = cy + dy * travel

        # =================================================
        # TRAIL
        # =================================================

        trail_length = 100 + random(0, 30)

        tail_x = px - dx * trail_length
        tail_y = py - dy * trail_length

        # =================================================
        # FADE
        # =================================================

        fade_start = constrain(progress * 10, 0, 1)
        fade_end = constrain((1 - progress) * 8, 0, 1)

        alpha = 255 * fade_start * fade_end

        # =================================================
        # COLOR
        # =================================================

        c = phase5_stream_colors[i]

        r = c[0]
        g = c[1]
        b = c[2]

        # =================================================
        # OUTER GLOW
        # =================================================

        stroke(r, g, b, alpha * 0.35)

        strokeWeight(10)

        line(tail_x, tail_y, px, py)

        # =================================================
        # MAIN ENERGY
        # =================================================

        stroke(r, g, b, alpha)

        strokeWeight(4)

        line(tail_x, tail_y, px, py)

        # =================================================
        # WHITE CORE
        # =================================================

        stroke(255, 255, 255, alpha * 0.7)

        strokeWeight(1.5)

        line(tail_x, tail_y, px, py)
        
# =====================================================
# PHASE 5 ACTIVATION EXPLOSION
# =====================================================

def start_phase5():

    global phase5_started
    global phase5_burst_start

    phase5_started = True
    phase5_burst_start = millis()

    # Create energy immediately
    create_phase5_energy()


def draw_phase5_explosion():

    elapsed = millis() - phase5_burst_start

    # Explosion duration
    duration = 700

    if elapsed >= duration:
        return

    # 0 -> 1
    t = elapsed / float(duration)

    # Strong flash at beginning
    if t < 0.15:

        flash = t / 0.15

        # Fade in very quickly
        alpha = 255 * flash

    else:

        # Fade out
        fade = 1 - ((t - 0.15) / 0.85)

        alpha = 255 * fade

    alpha = constrain(alpha, 0, 255)

    # -------------------------------------------------
    # WHITE POWER FLASH
    # -------------------------------------------------

    noStroke()

    fill(255, 255, 255, alpha * 0.85)

    rectMode(CORNER)
    rect(0, 0, w, h)

    rectMode(CENTER)

    # -------------------------------------------------
    # EXTRA CENTRAL BURST
    # -------------------------------------------------

    cx = field_w / 2
    cy = field_top + field_h / 2

    burst_size = 80 + t * 500

    fill(255, 255, 255, alpha * 0.30)

    ellipse(cx, cy, burst_size, burst_size)    
    
                        
# =========================================================
# PHASE 5 COSMIC STARS
# =========================================================

phase5_stars = []


def create_phase5_stars():

    global phase5_stars

    phase5_stars = []

    randomSeed(25)

    for i in range(80):

        sx = random(0, field_w)
        sy = random(field_top, field_bottom)
        brightness = random(40, 130)
        star_size = random(1, 3)

        phase5_stars.append({
            "x": sx,
            "y": sy,
            "brightness": brightness,
            "size": star_size
        })


def draw_phase5_stars():

    global phase5_stars

    # Create stars if they do not exist yet
    if len(phase5_stars) == 0:
        create_phase5_stars()

    noStroke()

    for star in phase5_stars:

        fill(255, 255, 255, star["brightness"])

        ellipse(star["x"], star["y"], star["size"], star["size"])
        
# =========================================================
# PHASE 5 COSMIC CENTER GLOW
# =========================================================

def draw_phase5_center_glow():

    cx = field_w / 2
    cy = field_top + field_h / 2

    pulse = (sin(millis() * 0.01) + 1) / 2

    noStroke()

    # Outer purple glow
    for i in range(6):

        size = 80 + i * 35 + pulse * 20
        alpha = 25 - i * 3

        fill(150, 80, 255, alpha)

        ellipse(cx, cy, size, size)

    # White energy glow
    for i in range(4):

        size = 45 + i * 18 + pulse * 10
        alpha = 40 - i * 7

        fill(220, 230, 255, alpha)

        ellipse(cx, cy, size, size)

    # Core

    fill(255)

    ellipse(cx, cy, 25 + pulse * 5, 25 + pulse * 5)   

# =========================================================
# PHASE 5 COSMIC FRAME
# =========================================================

def draw_phase5_cosmic_frame():

    pulse = (sin(millis() * 0.012) + 1) / 2

    noFill()

    # Outer purple glow

    for i in range(5):

        alpha = 45 - i * 7

        stroke(150, 80, 255, alpha)

        strokeWeight(3 + i * 3)

        rect(field_w / 2, field_top + field_h / 2, 
             field_w - 20 + i * 5, field_h - 20 + i * 5)

    # White core frame

    stroke(230, 230, 255, 150 + pulse * 100)

    strokeWeight(2)

    rect(field_w / 2, field_top + field_h / 2, field_w - 20, field_h - 20)
               
# =========================================================
# HIT PARTICLE
# =========================================================

particles = []


def create_hit_particles(hit_x, hit_y, direction):

    for i in range(10):

        # Particle flow
        spread = random(-PI / 3, PI / 3)

        if direction == "left":
            # spread right
            angle = spread

        else:
            # spread left
            angle = PI + spread

        speed = random(2, 5)

        particle = {
            "x": hit_x,
            "y": hit_y,
            "vx": cos(angle) * speed,
            "vy": sin(angle) * speed,
            "start": millis(),
            "life": random(100, 200),
            "size": random(2, 5)
        }

        particles.append(particle)


def update_hit_particles():

    for particle in particles[:]:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        if millis() - particle["start"] >= particle["life"]:
            particles.remove(particle)


def draw_hit_particles():

    noStroke()

    for particle in particles:

        elapsed = millis() - particle["start"]
        life = particle["life"]

        alpha = 255 * (1 - elapsed / life)

        fill(255, alpha)

        ellipse(
            particle["x"],
            particle["y"],
            particle["size"],
            particle["size"]
        )
        
def get_phase_name(phase):

    if phase == 1:
        return "NORMAL"

    elif phase == 2:
        return "HEATING?"

    elif phase == 3:
        return "BURNING!"

    elif phase == 4:
        return "!OVERDRIVE!"

    elif phase == 5:
        return "!!!SPEED OF LIGHT!!!"

    return "None"
        
def draw_player_ui():
    # Player 1
    fill(255)
    textAlign(CENTER, CENTER)

    textSize(24)
    text("PLAYER 1", 150, 35)

    textSize(20)
    text("COMBO: " + str(player1_combo), 150, 75)
    
    textSize(18)
    text("WIN STREAK: " + str(player1_win_streak), 150, 105)
    # Player 2
    textSize(24)
    text("PLAYER 2", 750, 35)

    textSize(20)
    text("COMBO: " + str(player2_combo), 750, 75)
    
    textSize(18)
    text("WIN STREAK: " + str(player2_win_streak), 750, 105)

def format_time():
    total_seconds = int(get_match_time() / 1000)

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return (
        ("0" + str(minutes) if minutes < 10 else str(minutes))
        + ":"
        + ("0" + str(seconds) if seconds < 10 else str(seconds))
    )

def format_previous_time():

    if previous_match_time is None:
        return "None"

    total_seconds = int(previous_match_time / 1000)

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return (
        ("0" + str(minutes) if minutes < 10 else str(minutes))
        + ":"
        + ("0" + str(seconds) if seconds < 10 else str(seconds))
    )
    
def draw_match_info_ui():
    fill(255)
    textAlign(CENTER, CENTER)

    # Round
    textSize(18)
    text("ROUND " + str(current_round), 330, 35)

    # Timer
    textSize(18)
    text("TIME " + format_time(), 450, 35)

    # Score
    textSize(24)
    text(str(player1_score) + " : " + str(player2_score), 570, 35)

def draw_key_ui():
    # Player 1
    draw_key("W", 230, 30, w_pressed)
    draw_key("S", 230, 75, s_pressed)

    # Player 2
    draw_key("UP", 670, 30, up_pressed)
    draw_key("DOWN", 670, 75, down_pressed)


def draw_key(label, x, y, pressed):
    rectMode(CENTER)

    if pressed:
        fill(255)
        stroke(255)
        strokeWeight(4)

    else:
        fill(30)
        stroke(150)
        strokeWeight(2)

    rect(x, y, 45, 35)

    fill(255)
    textAlign(CENTER, CENTER)
    textSize(18)

    text(label, x, y)


def draw_pause_button():
    if not paused and not resume_countdown and not quit_warning:
        draw_button("| |", pause_x, pause_y, pause_w, pause_h, 16)


def draw_button(label, x, y, button_w, button_h, text_size = 22):
    rectMode(CENTER)

    # Hover
    hovered = (
        x - button_w / 2 <= mouseX <= x + button_w / 2
        and
        y - button_h / 2 <= mouseY <= y + button_h / 2
    )

    if hovered:
        display_w = button_w + 8
        display_h = button_h + 8

        strokeWeight(4)
        textSize(text_size + 8)
        fill(100)

    else:
        display_w = button_w
        display_h = button_h

        strokeWeight(2)
        textSize(text_size)
        fill(40)

    stroke(255)

    rect(x, y, display_w, display_h)

    fill(255)
    textAlign(CENTER, CENTER)
    text(label, x, y)


# =========================================================
# MOUSE INPUT
# =========================================================

def mousePressed():
    global menu
    global previous_match_screen
    global countdown, countdown_start
    global paused
    global resume_countdown, resume_start
    global quit_warning, quit_warning_start
    global okay_pending
    global match_over, winner
    global goal_announcement
    global round_countdown, battle
    
    # -----------------------------------------------------
    # PREVIOUS MATCH SCREEN
    # -----------------------------------------------------

    if previous_match_screen:

        # BACK
        if (
            abs(mouseX - w / 2) <= 110
            and
            abs(mouseY - 585) <= 27.5
        ):

            previous_match_screen = False
            menu = True

            return

        return

    # -----------------------------------------------------
    # MENU
    # -----------------------------------------------------

    if menu:

        # PLAY
        if abs(mouseX - w / 2) <= 130:
            if abs(mouseY - 270) <= 30:

                menu = False
                previous_match_screen = False

                countdown = True
                countdown_start = millis()

                reset_match_data()
                reset_ball()

                return
    
    # PREVIOUS MATCH
        if abs(mouseX - w / 2) <= 130:
            if abs(mouseY - 370) <= 30:

                menu = False
                previous_match_screen = True

                return

        # EXIT
        if abs(mouseX - w / 2) <= 130:
            if abs(mouseY - 470) <= 30:
                exit()

        return


    # -----------------------------------------------------
    # MATCH END
    # -----------------------------------------------------

    if match_over:

        # REPLAY
        if (abs(mouseX - w / 2) <= 110 and abs(mouseY - 420) <= 27.5):
            reset_match()
            return


    # QUIT
    if (abs(mouseX - w / 2) <= 110 and abs(mouseY - 495) <= 27.5):
        match_over = False
        winner = 0

        reset_match_data()

        countdown = False
        goal_announcement = False
        round_countdown = False
        battle = False

        paused = False
        resume_countdown = False
        quit_warning = False

        menu = True
        return


    # -----------------------------------------------------
    # QUIT WARNING
    # -----------------------------------------------------

    if quit_warning:

        cancel_x = w / 2 - 130
        cancel_y = 400
        cancel_w = 200
        cancel_h = 55

        okay_x = w / 2 + 130
        okay_y = 400
        okay_w = 200
        okay_h = 55


        # CANCEL
        if (
            cancel_x - cancel_w / 2 <= mouseX <= cancel_x + cancel_w / 2
            and
            cancel_y - cancel_h / 2 <= mouseY <= cancel_y + cancel_h / 2
        ):
            quit_warning = False
            okay_pending = False
            return


        # OKAY
        if (
            okay_x - okay_w / 2 <= mouseX <= okay_x + okay_w / 2
            and
            okay_y - okay_h / 2 <= mouseY <= okay_y + okay_h / 2
        ):
            elapsed = millis() - quit_warning_start

            if elapsed >= 3000:
                reset_match_data()

                quit_warning = False
                okay_pending = False
                paused = False
                resume_countdown = False

                countdown = False
                goal_announcement = False
                round_countdown = False
                battle = False

                menu = True
                return

            else:
                okay_pending = True

            return

        return


    # -----------------------------------------------------
    # RESUME COUNTDOWN
    # -----------------------------------------------------

    if resume_countdown:
        return


    # -----------------------------------------------------
    # PAUSE BUTTON
    # -----------------------------------------------------

    if not paused:

        if (
            pause_x - pause_w / 2 <= mouseX <= pause_x + pause_w / 2
            and
            pause_y - pause_h / 2 <= mouseY <= pause_y + pause_h / 2
        ):

            if countdown:
                start_pause("countdown")

            elif goal_announcement:
                start_pause("goal")

            elif round_countdown:
                start_pause("round_countdown")

            else:
                start_pause("battle")

            return


    # -----------------------------------------------------
    # PAUSE FUNCTION
    # -----------------------------------------------------

    if paused:

        # RESUME
        if abs(mouseX - w / 2) <= 100:
            if abs(mouseY - (h / 2 + 20)) <= 27.5:
                start_resume()
                return


        # QUIT
        if abs(mouseX - w / 2) <= 110:
            if abs(mouseY - (h / 2 + 90)) <= 27.5:

                quit_warning = True
                quit_warning_start = millis()

                return

        return


# =========================================================
# KEYBOARD INPUT
# =========================================================

def keyPressed():
    global w_pressed, s_pressed
    global up_pressed, down_pressed

    if keyCode == 87:
        w_pressed = True

    if keyCode == 83:
        s_pressed = True

    if keyCode == UP:
        up_pressed = True

    if keyCode == DOWN:
        down_pressed = True


def keyReleased():
    global w_pressed, s_pressed
    global up_pressed, down_pressed

    if keyCode == 87:
        w_pressed = False

    if keyCode == 83:
        s_pressed = False

    if keyCode == UP:
        up_pressed = False

    if keyCode == DOWN:
        down_pressed = False


# =========================================================
# GAME LOGIC
# =========================================================

def draw_game():
    global x, y, vx, vy
    global left_y, right_y
    global field_top, field_bottom
    global paused
    global player1_win_streak, player2_win_streak
    global player1_combo, player2_combo
    global player1_max_combo, player2_max_combo
    global player1_win_streak, player2_win_streak
    global player1_score, player2_score
    global phase5_started
    global max_phase_reached

    draw_phase_background()
    draw_field()
    # Record maximum phase reached
    current_phase = get_heat_phase()

    if current_phase > max_phase_reached:
        max_phase_reached = current_phase
        
    # Phase 3 fire
    if get_heat_phase() == 3:
        heat = get_heat()
        phase_heat = (heat - 50) / 25
        phase_heat = constrain(phase_heat, 0, 1)

        draw_phase3_field_fire(phase_heat)

    # Phase 4 energy flow
    if get_heat_phase() == 4:

        heat = get_heat()

        phase_heat = (heat - 75) / 25
        phase_heat = constrain(phase_heat, 0, 1)

        draw_phase4_energy_flow(phase_heat)
        
    if get_heat_phase() == 5:

        # Trigger ONCE when entering Phase 5
        if not phase5_started:
            start_phase5()

        draw_phase5_stars()
        draw_phase5_cosmic_radiation()
        draw_phase5_center_glow()
        draw_phase5_cosmic_frame()

        # One-time activation explosion
        draw_phase5_explosion()

    else:

        # Allow Phase 5 to trigger again in a new match
        phase5_started = False

    draw_global_ui()
    update_hit_particles()
    draw_hit_particles()
   
    # -----------------------------------------------------
    # GAME LOGIC
    # -----------------------------------------------------

    if battle and not paused and not resume_countdown:

        # Ball movement
        x += vx
        y += vy


        # -------------------------------------------------
        # LEFT PADDLE COLLISION
        # -------------------------------------------------

        if x - radius <= left_x + paddle_w / 2 and vx < 0:

            if left_y - paddle_h / 2 <= y <= left_y + paddle_h / 2:

                player1_combo += 1
                
                if player1_combo > player1_max_combo:
                    player1_max_combo = player1_combo

                x = left_x + paddle_w / 2 + radius

                hit_pos = (y - left_y) / (paddle_h / 2)
                hit_pos = constrain(hit_pos, -1, 1)

                max_angle = PI / 3
                angle = hit_pos * max_angle

                speed = get_speed()

                vx = speed * cos(angle)
                vy = speed * sin(angle)

                vx = abs(vx)

                faster()
                create_hit_particles(left_x + paddle_w / 2 + radius, y, "left")


        # -------------------------------------------------
        # RIGHT PADDLE COLLISION
        # -------------------------------------------------

        if x + radius >= right_x - paddle_w / 2 and vx > 0:

            if right_y - paddle_h / 2 <= y <= right_y + paddle_h / 2:

                player2_combo += 1
                
                if player2_combo > player2_max_combo:
                    player2_max_combo = player2_combo

                x = right_x - paddle_w / 2 - radius

                hit_pos = (y - right_y) / (paddle_h / 2)
                hit_pos = constrain(hit_pos, -1, 1)

                max_angle = PI / 3
                angle = hit_pos * max_angle

                speed = get_speed()

                vx = -speed * cos(angle)
                vy = speed * sin(angle)

                vx = -abs(vx)

                faster()
                create_hit_particles(right_x - paddle_w / 2 - radius, y, "right")

        # -------------------------------------------------
        # TOP / BOTTOM BOUNCE
        # -------------------------------------------------

        if y - radius <= field_top:

            y = radius + field_top
            vy = abs(vy)

        elif y + radius >= field_bottom:

            y = field_bottom - radius
            vy = -abs(vy)


        # -------------------------------------------------
        # PADDLE MOVEMENT
        # -------------------------------------------------

        if w_pressed:
            left_y -= paddle_speed

        if s_pressed:
            left_y += paddle_speed

        if up_pressed:
            right_y -= paddle_speed

        if down_pressed:
            right_y += paddle_speed


    # -----------------------------------------------------
    # PADDLE BOUNDARY
    # -----------------------------------------------------

    left_y = constrain(
        left_y,
        field_top + paddle_h / 2,
        field_bottom - paddle_h / 2
    )

    right_y = constrain(
        right_y,
        field_top + paddle_h / 2,
        field_bottom - paddle_h / 2
    )

    # -----------------------------------------------------
    # TEST BARRIER
    # -----------------------------------------------------

    test_ball_barrier()

    # =================================================
    # GOAL DETECTION
    # =================================================

    if x < -radius:

        handle_goal(2, 0, y)
        return

    elif x > field_w + radius:

        handle_goal(1, field_w, y)
        return
    
    draw_game_objects()

# -----------------------------------------------------
# DRAW GAME OBJECTS
# -----------------------------------------------------
def draw_game_objects():
    draw_ball()
    draw_ball_trail()
    draw_paddles()
    
def draw_ball():
    phase = get_heat_phase()

    noStroke()
    
    if phase == 1:

        fill(255)
        ellipse(x, y, radius * 2, radius * 2)


    # Phase 2
    elif phase == 2:

        heat = get_heat()

        phase_heat = (heat - 25) / 25
        phase_heat = constrain(phase_heat, 0, 1)

        r = 255
        g = 255 - 135 * phase_heat
        b = 255 - 255 * phase_heat

        fill(r, g, b)

        ellipse(x, y, radius * 2, radius * 2)

    # Phase 3
    elif phase == 3:

        heat = get_heat()

        phase_heat = (heat - 50) / 25
        phase_heat = constrain(phase_heat, 0, 1)

        # Orange -> Blue
        r = 255 - 255 * phase_heat
        g = 120 + 135 * phase_heat
        b = 255 * phase_heat

        # MAIN BALL
        fill(r, g, b)
        ellipse(x, y, radius * 2, radius * 2)

        # Flame core
        core_r = 255 - 255 * phase_heat
        core_g = 220 + 35 * phase_heat
        core_b = 120 + 135 * phase_heat

        fill(core_r, core_g, core_b, 180)

        ellipse(x - vx / get_speed() * 5, y - vy / get_speed() * 5, radius, radius)
        
    # Phase 4
    elif phase == 4:

        heat = get_heat()

        phase_heat = (heat - 75) / 25
        phase_heat = constrain(phase_heat, 0, 1)

        # Outer aura
        aura_r = 40 + 150 * phase_heat
        aura_g = 140 + 100 * phase_heat
        aura_b = 255

        aura_size = radius * (3.5 + phase_heat * 1.5)

        fill(aura_r, aura_g, aura_b, 70)

        ellipse(x, y, aura_size, aura_size)

        # Main ball
        r = 120 + 135 * phase_heat
        g = 190 + 65 * phase_heat
        b = 255

        fill(r, g, b)

        ellipse(x, y, radius * 2, radius * 2)
        

    # PHASE 5 - LIGHT CORE


    else:

        pulse = (sin(millis() * 0.02) + 1) / 2

        noStroke()
        
        #outer light
        fill(220, 230, 255, 25)

        ellipse(x, y, radius * 6.0 + pulse * 8, radius * 6.0 + pulse * 8)
        
        #medium halo
        fill(230, 240, 255, 45)

        ellipse(x, y, radius * 4.0 + pulse * 5, radius * 4.0 + pulse * 5)
        
        #inner light

        fill(245, 250, 255, 100)

        ellipse(x, y, radius * 2.5, radius * 2.5)
        
       # white core

        fill(255, 255, 255, 255)

        ellipse(x, y, radius * 1.5, radius * 1.5)
        
def draw_ball_trail():

    phase = get_heat_phase()

    # =====================================================
    # PHASE 2
    # =====================================================

    if phase == 2:

        heat = get_heat()

        phase_heat = (heat - 25) / 25
        phase_heat = constrain(phase_heat, 0, 1)

        trail_length = 10 + 15 * phase_heat

        speed = get_speed()

        trail_x = x - vx / speed * trail_length
        trail_y = y - vy / speed * trail_length

        noStroke()
        fill(255, 120, 0, 60)

        ellipse(trail_x, trail_y, radius * 1.3, radius * 1.3)


    # =====================================================
    # PHASE 3
    # =====================================================

    # Phase 3
    elif phase == 3:

        heat = get_heat()

        phase_heat = (heat - 50) / 25
        phase_heat = constrain(phase_heat, 0, 1)

        # Orange -> Blue
        r = 255 - 255 * phase_heat
        g = 120 + 135 * phase_heat
        b = 255 * phase_heat

        # Soft glow
        fill(r, g, b, 45)
        ellipse(x, y, radius * 3.0, radius * 3.0)

        # Main ball
        fill(r, g, b)
        ellipse(x, y, radius * 2, radius * 2)

        # Core
        core_r = 255 - 255 * phase_heat
        core_g = 220 + 35 * phase_heat
        core_b = 120 + 135 * phase_heat

        fill(core_r, core_g, core_b, 170)

        ellipse(x - vx / get_speed() * 4, 
                y - vy / get_speed() * 4, 
                radius * 0.8, radius * 0.8)
        
    # =====================================================
    # PHASE 4
    # =====================================================

    elif phase == 4:

        heat = get_heat()

        # 75% -> 100%
        phase_heat = (heat - 75) / 25
        phase_heat = constrain(phase_heat, 0, 1)

        speed = get_speed()

        # more spped more length
        trail_length = 45 + 55 * phase_heat

        # Blue -> Pale Blue
        r = 70 + 130 * phase_heat
        g = 170 + 60 * phase_heat
        b = 255

        # opposite side of moving ball
        dir_x = vx / speed
        dir_y = vy / speed

        trail_x = x - dir_x * trail_length
        trail_y = y - dir_y * trail_length

        noStroke()

        # Main stretched energy
        fill(r, g, b, 70)

        ellipse(trail_x, trail_y, radius * 1.4, radius * 1.4)

        # Core streak
        fill(220, 245, 255, 120)

        ellipse(x - dir_x * trail_length * 0.45, 
                y - dir_y * trail_length * 0.45,
                radius * 0.8, radius * 0.8)
        
    # =====================================================
    # PHASE 5
    # =====================================================

    elif phase == 5:

        speed = get_speed()

        if speed == 0:
            return

        # -------------------------------------------------
        # TRAIL LENGTH
        # -------------------------------------------------

        light_trail_length = 140

        # -------------------------------------------------
        # MOVEMENT DIRECTION
        # -------------------------------------------------

        dir_x = vx / speed
        dir_y = vy / speed

        noStroke()

        # OUTER GLOW

        for i in range(8):

            t = i / 8.0

            trail_x = x - dir_x * light_trail_length * t
            trail_y = y - dir_y * light_trail_length * t

            glow_alpha = 45 * (1 - t)

            glow_size = radius * (2.8 - t * 1.8)

            fill(170, 220, 255, glow_alpha)

            ellipse(trail_x, trail_y, glow_size, glow_size)

        # MAIN LIGHT

        for i in range(10):

            t = i / 10.0

            trail_x = x - dir_x * light_trail_length * t
            trail_y = y - dir_y * light_trail_length * t

            light_alpha = 110 * (1 - t)

            light_size = radius * (1.5 - t * 0.9)

            fill(220, 240, 255, light_alpha)

            ellipse(trail_x, trail_y, light_size, light_size)

        # WHITE CORE

        for i in range(6):

            t = i / 6.0

            trail_x = x - dir_x * light_trail_length * 0.75 * t
            trail_y = y - dir_y * light_trail_length * 0.75 * t

            core_alpha = 210 * (1 - t)

            core_size = radius * (0.75 - t * 0.45)

            fill(255, 255, 255, core_alpha)

            ellipse(trail_x, trail_y, core_size, core_size)
            
def draw_ball_at(ball_x, ball_y):
    noStroke()
    fill(255)
    ellipse(ball_x, ball_y, radius * 2, radius * 2)
    
def draw_paddles():
    # Paddles
    noStroke()
    fill(255)
    #left
    rect(left_x, left_y, paddle_w, paddle_h)
    #right
    rect(right_x, right_y, paddle_w, paddle_h)


# =========================================================
# PHYSICS / UTILITY
# =========================================================

def test_ball_barrier():
    global x, vx

    if not test_barrier:
        return

    # Left barrier
    if x - radius <= 0:
        x = radius
        vx = abs(vx)

    # Right barrier
    elif x + radius >= field_w:
        x = field_w - radius
        vx = -abs(vx)
        
def faster():
    current_speed = get_speed()

    new_speed = current_speed + a

    if new_speed >= vm:
        new_speed = vm

    set_speed(new_speed)

def get_speed():
    return sqrt(vx ** 2 + vy ** 2)

def set_speed(target_speed):
    global vx, vy

    current_speed = get_speed()

    if current_speed == 0:
        return

    target_speed = constrain(target_speed, 0, vm)

    vx = vx / current_speed * target_speed
    vy = vy / current_speed * target_speed
