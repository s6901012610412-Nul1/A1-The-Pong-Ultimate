/**
 * The Pong Ultimate — Processing Java Mode migration.
 * Organized by state/lifecycle, screens, game logic, HUD, effects, and input.
 * Source audit and build checklist: see sibling MIGRATION_MAP.md and BUILD_AND_TEST.md.
 */

// Core game state (names retained from Python where practical)
boolean menu = true;
boolean previous_match_screen = false;
boolean paused = false;
String pause_state = "";
boolean countdown = false;
boolean goal_announcement = false;
boolean round_countdown = false;
boolean battle = false;
boolean match_over = false;
boolean resume_countdown = false;
boolean quit_warning = false;
boolean okay_pending = false;
boolean test_barrier = false;

int countdown_start = 0;
int goal_announcement_start = 0;
int pause_x = 35, pause_y = 30, pause_w = 50, pause_h = 30;
int goal_player = 0;
int winner = 0;
int pause_started = 0;
int pause_frozen_elapsed = 0;
int resume_start = 0;
int round_countdown_start = 0;
int quit_warning_start = 0;
int current_round = 1;
int player1_win_streak = 0, player2_win_streak = 0;
int player1_max_win_streak = 0, player2_max_win_streak = 0;
int max_phase_reached = 1;
boolean previous_match_exists = false;
boolean phase5_started = false;

int phase5_burst_start = 0;
boolean phase5_fps_measuring = false;
int phase5_fps_session_start = 0, phase5_fps_window_start = 0, phase5_fps_last_log = 0;
int phase5_fps_window_frames = 0, phase5_fps_total_frames = 0, phase5_fps_samples = 0;
float phase5_fps_current = 0, phase5_fps_average = 0, phase5_fps_min = Float.MAX_VALUE, phase5_fps_max = 0;
Integer previous_winner = null, previous_player1_score = null, previous_player2_score = null;
Integer previous_match_time = null, previous_player1_max_combo = null, previous_player2_max_combo = null;
Integer previous_player1_max_win_streak = null, previous_player2_max_win_streak = null, previous_max_phase = null;

int player1_score = 0;
int player2_score = 0;
int score_limit = 5;
int player1_combo = 0;
int player2_combo = 0;
int player1_max_combo = 0;
int player2_max_combo = 0;

int w = 900;
int h = 650;
int field_w = 900;
int field_h = 500;
int field_top = 150;
int field_bottom = field_top + field_h;

float x = field_w / 2.0f;
float y = field_top + field_h / 2.0f;
float vx = 0;
float vy = 0;
float radius = 15;
float goal_x = x;
float goal_y = y;
float end_x = x, end_y = y;
float a = 0.25f;
float vm = 30;
float paddle_w = 10;
float paddle_h = 150;
float left_x = 30;
float left_y = field_top + field_h / 2.0f;
float right_x = field_w - 30;
float right_y = field_top + field_h / 2.0f;
float paddle_speed = 20;

boolean w_pressed = false;
boolean s_pressed = false;
boolean up_pressed = false;
boolean down_pressed = false;

int match_timer = 0;
int timer_start = 0;
boolean timer_running = false;

public void setup() {
  size(900, 650);
  ellipseMode(CENTER);
  rectMode(CENTER);
  stroke(255);
  strokeWeight(4);
  noFill();
  reset_ball();
}

public void draw() {
  // Preserve the Python dispatcher priority and early returns.
  if (previous_match_screen) {
    draw_previous_match();
    return;
  }
  if (menu) {
    draw_menu();
    return;
  }
  if (match_over) {
    draw_match_end();
    return;
  }
  if (resume_countdown) {
    if (pause_state.equals("battle")) draw_game();
    else {
      background(20);
      draw_field();
      draw_global_ui();
      draw_paddles();
    }
    draw_resume_countdown();
    return;
  }
  if (countdown) draw_countdown();
  else if (goal_announcement) draw_goal_announcement();
  else if (round_countdown) draw_round_countdown();
  else draw_game();

  if (quit_warning) draw_pause_overlay();
  else if (paused) draw_pause_overlay();
}

// SCREENS: menu, countdown, goal, round, match-end, history, pause
void draw_menu() {
  background(20);
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(48);
  text("THE PONG ULTIMATE", w/2, 120);
  draw_button("PLAY", w/2, 270, 260, 60);
  draw_button("PREVIOUS MATCH", w/2, 370, 260, 60);
  draw_button("EXIT", w/2, 470, 260, 60);
}

void draw_countdown() {
  background(20);
  draw_field();
  draw_global_ui();
  draw_paddles();
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(80);
  int elapsed = get_phase_elapsed(countdown_start);
  if (elapsed < 1000) text("3", w / 2, field_top + field_h / 2);
  else if (elapsed < 2000) text("2", w / 2, field_top + field_h / 2);
  else if (elapsed < 3000) text("1", w / 2, field_top + field_h / 2);
  else if (elapsed < 4000) text("BATTLE!", w / 2, field_top + field_h / 2);
  else {
    countdown = false;
    battle = true;
    start_timer();
  }
}

void draw_goal_announcement() {
  int elapsed = get_phase_elapsed(goal_announcement_start);
  background(20);
  draw_field();
  draw_paddles();
  draw_global_ui();
  draw_ball_at(goal_x, goal_y);
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(60);
  text(goal_player == 1 ? "PLAYER 1 GOAL!" : "PLAYER 2 GOAL!", w / 2, field_top + field_h / 2);
  if (elapsed >= 3000) {
    goal_announcement = false;
    current_round++;
    reset_ball();
    round_countdown = true;
    round_countdown_start = millis();
  }
}

void draw_round_countdown() {
  int elapsed = get_phase_elapsed(round_countdown_start);
  background(20);
  draw_field();
  draw_global_ui();
  draw_paddles();
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(80);
  if (elapsed < 1000) text("3", w / 2, field_top + field_h / 2);
  else if (elapsed < 2000) text("2", w / 2, field_top + field_h / 2);
  else if (elapsed < 3000) text("1", w / 2, field_top + field_h / 2);
  else if (elapsed < 4000) text("BATTLE!", w / 2, field_top + field_h / 2);
  else {
    round_countdown = false;
    battle = true;
    start_timer();
  }
}

void draw_match_end() {
  background(20);
  draw_field();
  draw_paddles();
  draw_ball_at(end_x, end_y);
  draw_global_ui();
  rectMode(CENTER);
  fill(20);
  stroke(255);
  strokeWeight(3);
  rect(w/2, 400, 450, 300);
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(60);
  text(winner==1?"PLAYER 1 WINS!":"PLAYER 2 WINS!", w/2, 325);
  draw_button("REPLAY", w/2, 420, 220, 55);
  draw_button("QUIT", w/2, 495, 220, 55);
}

void draw_field() {
  stroke(255);
  noFill();
  strokeWeight(3);
  rect(field_w/2.0f, field_top+field_h/2.0f, field_w-20, field_h-20);
  strokeWeight(1);
  rect(field_w/2.0f, field_top+field_h/2.0f, field_w-30, field_h-30);
  strokeWeight(2);
  for (int lineY=field_top+20; lineY<field_bottom-20; lineY+=24)line(field_w/2.0f, lineY, field_w/2.0f, lineY+12);
}

void draw_score() {
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(30);
  text(player1_score + "    :    " + player2_score, width / 2, 85);
}

// GAME LOGIC: update, collision, scoring, boundaries, and goal detection
void draw_game() {
  draw_phase_background();
  draw_field();
  int phaseNow = get_heat_phase();
  if (phaseNow > max_phase_reached) max_phase_reached = phaseNow;
  if (phaseNow == 3) draw_phase3_field_fire(constrain((get_heat()-50)/25, 0, 1));
  if (phaseNow == 4) draw_phase4_energy_flow(constrain((get_heat()-75)/25, 0, 1));
  if (phaseNow == 5) {
    if (!phase5_started) start_phase5();
    draw_phase5_stars();
    draw_phase5_cosmic_radiation();
    draw_phase5_center_glow();
    draw_phase5_cosmic_frame();
    draw_phase5_explosion();
  } else phase5_started = false;
  update_phase5_fps(phaseNow);
draw_global_ui();
  update_hit_particles();
  draw_hit_particles();

  if (battle && !paused && !resume_countdown) {
    x += vx;
    y += vy;
    collide_with_paddles();
    if (y-radius <= field_top) {
      y=radius+field_top;
      vy=abs(vy);
    } else if (y+radius >= field_bottom) {
      y=field_bottom-radius;
      vy=-abs(vy);
    }
    if (w_pressed) left_y -= paddle_speed;
    if (s_pressed) left_y += paddle_speed;
    if (up_pressed) right_y -= paddle_speed;
    if (down_pressed) right_y += paddle_speed;
  }
  left_y=constrain(left_y, field_top+paddle_h/2, field_bottom-paddle_h/2);
  right_y=constrain(right_y, field_top+paddle_h/2, field_bottom-paddle_h/2);
  test_ball_barrier();
  if (x < -radius) {
    handle_goal(2, 0, y);
    return;
  } else if (x > field_w+radius) {
    handle_goal(1, field_w, y);
    return;
  }
  draw_game_objects();

}

void collide_with_paddles() {
  if (x-radius <= left_x+paddle_w/2 && vx<0 && y>=left_y-paddle_h/2 && y<=left_y+paddle_h/2) {
    player1_combo++;
    player1_max_combo=max(player1_max_combo, player1_combo);
    x=left_x+paddle_w/2+radius;
    float hit=constrain((y-left_y)/(paddle_h/2), -1, 1), speed=get_speed(), angle=hit*PI/3;
    vx=abs(speed*cos(angle));
    vy=speed*sin(angle);
    faster();
    create_hit_particles(left_x+paddle_w/2+radius, y, "left");
  }
  if (x+radius >= right_x-paddle_w/2 && vx>0 && y>=right_y-paddle_h/2 && y<=right_y+paddle_h/2) {
    player2_combo++;
    player2_max_combo=max(player2_max_combo, player2_combo);
    x=right_x-paddle_w/2-radius;
    float hit=constrain((y-right_y)/(paddle_h/2), -1, 1), speed=get_speed(), angle=hit*PI/3;
    vx=-abs(speed*cos(angle));
    vy=speed*sin(angle);
    faster();
    create_hit_particles(right_x-paddle_w/2-radius, y, "right");
  }
}

void draw_paddles() {
  noStroke();
  fill(255);
  rect(left_x, left_y, paddle_w, paddle_h);
  rect(right_x, right_y, paddle_w, paddle_h);
}

void draw_ball_and_paddles() {
  draw_game_objects();

}

void reset_ball() {
  x = field_w / 2.0f;
  y = field_top + field_h / 2.0f;
  float angle = random(-PI / 4, PI / 4);
  if (random(1) < 0.5) angle = PI - angle;
  vx = 5 * cos(angle);
  vy = 5 * sin(angle);
}

void reset_paddles() {
  left_y = field_top + field_h / 2.0f;
  right_y = field_top + field_h / 2.0f;
}

void reset_match_data() {
  phase5_started=false;
  phase5_stream_progress=new float[0];
  phase5_stream_colors=new int[0][0];
  phase5_stream_angles=new float[0];
  player1_score=0;
  player2_score=0;
  player1_combo=0;
  player2_combo=0;
  player1_win_streak=0;
  player2_win_streak=0;
  player1_max_combo=0;
  player2_max_combo=0;
  player1_max_win_streak=0;
  player2_max_win_streak=0;
  max_phase_reached=1;
  current_round=1;
  reset_paddles();
  reset_timer();
}

void reset_match() {
  menu = false;
  countdown = true;
  countdown_start = millis();
  match_over = false;
  winner = 0;
  paused = false;
  resume_countdown = false;
  quit_warning = false;
  okay_pending = false;
  goal_announcement = false;
  round_countdown = false;
  battle = false;
  reset_match_data();
  reset_ball();
}

void handle_goal(int player, float last_x, float last_y) {
  stop_timer();
  process_goal(player);
  if (player==1 && player1_score>=score_limit) start_match_end(1, last_x, last_y);
  else if (player==2 && player2_score>=score_limit) start_match_end(2, last_x, last_y);
  else start_goal(player, last_x, last_y);
}
void process_goal(int player) {
  if (player==2) {
    player2_score++;
    player1_combo=0;
    player2_win_streak++;
    player2_max_win_streak=max(player2_max_win_streak, player2_win_streak);
    player1_win_streak=0;
  } else {
    player1_score++;
    player2_combo=0;
    player1_win_streak++;
    player1_max_win_streak=max(player1_max_win_streak, player1_win_streak);
    player2_win_streak=0;
  }
}
void start_goal(int player, float last_x, float last_y) {
  goal_player=player;
  goal_x=last_x;
  goal_y=last_y;
  battle=false;
  countdown=false;
  round_countdown=false;
  goal_announcement=true;
  goal_announcement_start=millis();
  x=field_w/2.0f;
  y=field_top+field_h/2.0f;
  vx=0;
  vy=0;
}
void start_match_end(int player, float last_x, float last_y) {
  winner=player;
  match_over=true;
  battle=false;
  end_x=last_x;
  end_y=last_y;
  vx=0;
  vy=0;
  stop_timer();
  save_previous_match();
}

void start_timer() {
  if (!timer_running) {
    timer_start = millis();
    timer_running = true;
  }
}

void stop_timer() {
  if (timer_running) {
    match_timer += millis() - timer_start;
    timer_running = false;
  }
}

void reset_timer() {
  match_timer = 0;
  timer_start = 0;
  timer_running = false;
}

int get_match_time() {
  return timer_running ? match_timer + millis() - timer_start : match_timer;
}

float get_speed() {
  return sqrt(vx * vx + vy * vy);
}

void faster() {
  set_speed(min(get_speed() + a, vm));
}

void set_speed(float target_speed) {
  float current_speed = get_speed();
  if (current_speed == 0) return;
  target_speed = constrain(target_speed, 0, vm);
  vx = vx / current_speed * target_speed;
  vy = vy / current_speed * target_speed;
}

void test_ball_barrier() {
  if (!test_barrier) return;
  if (x - radius <= 0) {
    x = radius;
    vx = abs(vx);
  } else if (x + radius >= field_w) {
    x = field_w - radius;
    vx = -abs(vx);
  }
}









// =========================================================
// SCREEN / PAUSE / INPUT SUPPORT (ported from source)
// =========================================================

void draw_previous_match() {
  background(20);
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(42);
  text("PREVIOUS MATCH", w / 2, 70);
  rectMode(CENTER);
  fill(20);
  stroke(255);
  strokeWeight(3);
  rect(w / 2, 350, 650, 500);
  fill(255);
  noStroke();
  textSize(24);
  if (!previous_match_exists) {
    text("WINNER: None", w / 2, 150);
    text("SCORE: None", w / 2, 200);
    text("TIME: None", w / 2, 250);
    text("PLAYER 1 MAX COMBO: None", w / 2, 310);
    text("PLAYER 2 MAX COMBO: None", w / 2, 350);
    text("PLAYER 1 MAX WIN STREAK: None", w / 2, 410);
    text("PLAYER 2 MAX WIN STREAK: None", w / 2, 450);
    text("MAX PHASE: None", w / 2, 510);
  } else {
    text("WINNER: PLAYER " + previous_winner, w / 2, 150);
    text("SCORE: " + previous_player1_score + " : " + previous_player2_score, w / 2, 200);
    text("TIME: " + format_previous_time(), w / 2, 250);
    text("PLAYER 1 MAX COMBO: " + previous_player1_max_combo, w / 2, 310);
    text("PLAYER 2 MAX COMBO: " + previous_player2_max_combo, w / 2, 350);
    text("PLAYER 1 MAX WIN STREAK: " + previous_player1_max_win_streak, w / 2, 410);
    text("PLAYER 2 MAX WIN STREAK: " + previous_player2_max_win_streak, w / 2, 450);
    text("MAX PHASE: " + previous_max_phase + " - " + get_phase_name(previous_max_phase), w / 2, 510);
  }
  draw_button("BACK", w / 2, 585, 220, 55);
}

void draw_pause_screen() {
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(50);
  text("GAME PAUSED", w / 2, h / 2 - 70);
  draw_button("RESUME", w / 2, h / 2 + 20, 220, 55);
  draw_button("QUIT", w / 2, h / 2 + 90, 220, 55);
}

void draw_resume_countdown() {
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(80);
  int elapsed = millis() - resume_start;
  if (elapsed < 1000) text("3", w / 2, field_top + field_h / 2);
  else if (elapsed < 2000) text("2", w / 2, field_top + field_h / 2);
  else if (elapsed < 3000) text("1", w / 2, field_top + field_h / 2);
  else if (elapsed < 4000) text("BATTLE!", w / 2, field_top + field_h / 2);
  else finish_resume();
}

void draw_pause_overlay() {
  fill(0, 150);
  noStroke();
  rectMode(CORNER);
  rect(0, 0, w, h);
  rectMode(CENTER);
  if (quit_warning) draw_quit_warning();
  else if (paused) draw_pause_screen();
}

void draw_quit_warning() {
  int elapsed = millis() - quit_warning_start;
  if (okay_pending && elapsed >= 3000) {
    reset_match_data();
    quit_warning = false;
    okay_pending = false;
    paused = false;
    resume_countdown = false;
    menu = true;
    return;
  }
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(50);
  text("WARNING!", w / 2, 180);
  textSize(22);
  text("THIS ACTION WILL MAKE YOU LOSE PROGRESS", w / 2, 250);
  text("ARE YOU SURE?", w / 2, 285);
  draw_button("CANCEL", w / 2 - 130, 400, 200, 55);
  if (elapsed >= 3000) draw_button("OKAY", w / 2 + 130, 400, 200, 55);
  else {
    rectMode(CENTER);
    stroke(100);
    strokeWeight(2);
    fill(30);
    rect(w / 2 + 130, 400, 200, 55);
    fill(100);
    textSize(22);
    text("OKAY", w / 2 + 130, 400);
  }
}

int get_phase_elapsed(int start_time) {
  return paused ? pause_frozen_elapsed : millis() - start_time;
}

void start_pause(String state) {
  if (paused) return;
  paused = true;
  pause_started = millis();
  pause_state = state;
  stop_timer();
  w_pressed = false;
  s_pressed = false;
  up_pressed = false;
  down_pressed = false;
  if (state.equals("countdown")) pause_frozen_elapsed = millis() - countdown_start;
  else if (state.equals("goal")) pause_frozen_elapsed = millis() - goal_announcement_start;
  else if (state.equals("round_countdown")) pause_frozen_elapsed = millis() - round_countdown_start;
  else if (state.equals("battle")) pause_frozen_elapsed = 0;
}

void start_resume() {
  if (!paused) return;
  resume_countdown = true;
  resume_start = millis();
}

void finish_resume() {
  if (pause_state.equals("countdown") || pause_state.equals("goal") || pause_state.equals("round_countdown")) {
    countdown = false;
    goal_announcement = false;
    round_countdown = false;
    reset_ball();
    battle = true;
    start_timer();
  } else if (pause_state.equals("battle")) {
    battle = true;
    start_timer();
  }
  paused = false;
  resume_countdown = false;
}

void draw_button(String label, float bx, float by, float bw, float bh) {
  draw_button(label, bx, by, bw, bh, 22);
}

void draw_button(String label, float bx, float by, float bw, float bh, int size) {
  rectMode(CENTER);
  boolean hovered = bx - bw/2 <= mouseX && mouseX <= bx + bw/2 && by - bh/2 <= mouseY && mouseY <= by + bh/2;
  float dw = hovered ? bw + 8 : bw, dh = hovered ? bh + 8 : bh;
  strokeWeight(hovered ? 4 : 2);
  textSize(hovered ? size + 8 : size);
  fill(hovered ? 100 : 40);
  stroke(255);
  rect(bx, by, dw, dh);
  fill(255);
  textAlign(CENTER, CENTER);
  text(label, bx, by);
}

public void mousePressed() {
  if (previous_match_screen) {
    if (abs(mouseX - w/2) <= 110 && abs(mouseY - 585) <= 27.5) {
      previous_match_screen = false;
      menu = true;
    }
    return;
  }
  if (menu) {
    if (abs(mouseX-w/2)<=130 && abs(mouseY-270)<=30) {
      menu=false;
      previous_match_screen=false;
      countdown=true;
      countdown_start=millis();
      reset_match_data();
      reset_ball();
      return;
    }
    if (abs(mouseX-w/2)<=130 && abs(mouseY-370)<=30) {
      menu=false;
      previous_match_screen=true;
      return;
    }
    if (abs(mouseX-w/2)<=130 && abs(mouseY-470)<=30) {
      exit();
      return;
    }
    return;
  }
  if (match_over) {
    if (abs(mouseX-w/2)<=110 && abs(mouseY-420)<=27.5) {
      reset_match();
      return;
    }
    if (abs(mouseX-w/2)<=110 && abs(mouseY-495)<=27.5) {
      match_over=false;
      winner=0;
      reset_match_data();
      countdown=false;
      goal_announcement=false;
      round_countdown=false;
      battle=false;
      paused=false;
      resume_countdown=false;
      quit_warning=false;
      menu=true;
      return;
    }
  }
  if (quit_warning) {
    boolean cancel = mouseX >= w/2-230 && mouseX <= w/2-30 && mouseY >= 372.5 && mouseY <= 427.5;
    boolean okay = mouseX >= w/2+30 && mouseX <= w/2+230 && mouseY >= 372.5 && mouseY <= 427.5;
    if (cancel) {
      quit_warning=false;
      okay_pending=false;
      return;
    }
    if (okay) {
      if (millis()-quit_warning_start >= 3000) {
        reset_match_data();
        quit_warning=false;
        okay_pending=false;
        paused=false;
        resume_countdown=false;
        countdown=false;
        goal_announcement=false;
        round_countdown=false;
        battle=false;
        menu=true;
      } else okay_pending=true;
    }
    return;
  }
  if (resume_countdown) return;
  if (!paused && mouseX >= pause_x-pause_w/2 && mouseX <= pause_x+pause_w/2 && mouseY >= pause_y-pause_h/2 && mouseY <= pause_y+pause_h/2) {
    if (countdown) start_pause("countdown");
    else if (goal_announcement) start_pause("goal");
    else if (round_countdown) start_pause("round_countdown");
    else start_pause("battle");
    return;
  }
  if (paused) {
    if (abs(mouseX-w/2)<=100 && abs(mouseY-(h/2+20))<=27.5) {
      start_resume();
      return;
    }
    if (abs(mouseX-w/2)<=110 && abs(mouseY-(h/2+90))<=27.5) {
      quit_warning=true;
      quit_warning_start=millis();
      return;
    }
  }
}



// =========================================================
// STATS / HUD / TIME FORMATTING (Stage D baseline)
// =========================================================

void save_previous_match() {
  previous_match_exists = true;
  previous_winner = winner;
  previous_player1_score = player1_score;
  previous_player2_score = player2_score;
  previous_match_time = get_match_time();
  previous_player1_max_combo = player1_max_combo;
  previous_player2_max_combo = player2_max_combo;
  previous_player1_max_win_streak = player1_max_win_streak;
  previous_player2_max_win_streak = player2_max_win_streak;
  previous_max_phase = max_phase_reached;
}

float get_heat() {
  float speed = get_speed();
  if (speed >= vm - 0.001f) return 100;
  return constrain((speed - 5) / 25 * 100, 0, 100);
}

int get_heat_phase() {
  float heatValue = get_heat();
  if (heatValue < 25) return 1;
  if (heatValue < 50) return 2;
  if (heatValue < 75) return 3;
  if (heatValue < 100) return 4;
  return 5;
}

String get_phase_name(int phase) {
  if (phase == 1) return "NORMAL";
  if (phase == 2) return "HEATING?";
  if (phase == 3) return "BURNING!";
  if (phase == 4) return "!OVERDRIVE!";
  if (phase == 5) return "!!!SPEED OF LIGHT!!!";
  return "None";
}

String format_time() {
  return format_millis(get_match_time());
}
String format_previous_time() {
  return previous_match_time == null ? "None" : format_millis(previous_match_time);
}
String format_millis(int elapsed) {
  int seconds = elapsed / 1000;
  int minutes = seconds / 60;
  seconds %= 60;
  return nf(minutes, 2) + ":" + nf(seconds, 2);
}

void draw_global_ui() {
  draw_player_ui();
  draw_key_ui();
  draw_match_info_ui();
  draw_heat_ui();
  draw_pause_button();
  draw_fps_ui();
}
void draw_player_ui() {
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(24);
  text("PLAYER 1", 150, 35);
  textSize(20);
  text("COMBO: " + player1_combo, 150, 75);
  textSize(18);
  text("WIN STREAK: " + player1_win_streak, 150, 105);
  textSize(24);
  text("PLAYER 2", 750, 35);
  textSize(20);
  text("COMBO: " + player2_combo, 750, 75);
  textSize(18);
  text("WIN STREAK: " + player2_win_streak, 750, 105);
}
void draw_key_ui() {
  draw_key("W", 230, 30, w_pressed);
  draw_key("S", 230, 75, s_pressed);
  draw_key("UP", 670, 30, up_pressed);
  draw_key("DOWN", 670, 75, down_pressed);
}
void draw_key(String label, float kx, float ky, boolean pressed) {
  rectMode(CENTER);
  fill(pressed ? 255 : 30);
  stroke(pressed ? 255 : 150);
  strokeWeight(pressed ? 4 : 2);
  rect(kx, ky, 45, 35);
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(18);
  text(label, kx, ky);
}
void draw_match_info_ui() {
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(18);
  text("ROUND " + current_round, 330, 35);
  text("TIME " + format_time(), 450, 35);
  textSize(24);
  text(player1_score + " : " + player2_score, 570, 35);
}
void draw_heat_ui() {
  float heatValue=get_heat();
  int phase=get_heat_phase();
  float bx=w/2.0f, by=95, bw=300, bh=18;
  rectMode(CENTER);
  stroke(150);
  strokeWeight(2);
  fill(30);
  rect(bx, by, bw, bh);
  fill(255);
  noStroke();
  float hw=bw*(heatValue/100);
  rect(bx-bw/2+hw/2, by, hw, bh);
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(16);
  text("HEAT " + (int)heatValue + "%", bx, by-18);
  text("PHASE " + phase + ": " + get_phase_name(phase), bx, by+28);
}
void draw_pause_button() {
  if (!paused && !resume_countdown && !quit_warning) draw_button("| |", pause_x, pause_y, pause_w, pause_h, 16);
}
void draw_fps_ui() {
  fill(255);
  textAlign(CENTER, CENTER);
  textSize(16);
  text("FPS " + (int)frameRate, w-pause_x, pause_y-12);
}
void draw_ball_at(float bx, float by) {
  noStroke();
  fill(255);
  ellipse(bx, by, radius*2, radius*2);
}




// =========================================================
// VISUAL EFFECTS: phase backgrounds, streams, ball, stars, particles
// =========================================================

float[] phase4_stream_progress = new float[0];
final int phase4_stream_count = 15;
float[] phase5_stream_progress = new float[0];
float[] phase5_stream_angles = new float[0];
float[] phase5_stream_dx = new float[0];
float[] phase5_stream_dy = new float[0];
float[] phase5_stream_edge_distance = new float[0];
int[][] phase5_stream_colors = new int[0][0];
PGraphics phase5_star_layer = null;
final int[][] PHASE5_COLORS = {{255,70,70},{255,140,40},{255,220,70},{70,180,255},{80,255,220},{130,90,255},{220,80,255},{255,255,255}};
final int phase5_stream_count = 15;
ArrayList<Star> phase5_stars = new ArrayList<Star>();
ArrayList<HitParticle> particles = new ArrayList<HitParticle>();

class Star {
  float x, y, brightness, size;
  Star(float x, float y, float b, float s) {
    this.x=x;
    this.y=y;
    brightness=b;
    size=s;
  }
}
class HitParticle {
  float x, y, vx, vy, size;
  int start, life;
  HitParticle(float x, float y, float vx, float vy, int start, int life, float size) {
    this.x=x;
    this.y=y;
    this.vx=vx;
    this.vy=vy;
    this.start=start;
    this.life=life;
    this.size=size;
  }
}

void draw_phase_background() {
  float heatValue=get_heat(), t, r, g, b;
  if (heatValue<25) {
    t=constrain(heatValue/25, 0, 1);
    r=20+25*t;
    g=20+10*t;
    b=20;
  } else if (heatValue<50) {
    t=constrain((heatValue-25)/25, 0, 1);
    r=45+10*t;
    g=30-5*t;
    b=20-5*t;
  } else if (heatValue<75) {
    t=constrain((heatValue-50)/25, 0, 1);
    r=55-40*t;
    g=25+15*t;
    b=15+50*t;
  } else if (heatValue>=100) {
    background(8, 3, 18);
    return;
  } else {
    t=constrain((heatValue-75)/25, 0, 1);
    r=15-5*t;
    g=40+15*t;
    b=65+45*t;
  }
  background(r, g, b);
}

void draw_phase3_field_fire(float phaseHeat) {
  float intensity=1+phaseHeat, fr=255-255*phaseHeat, fg=120+135*phaseHeat, fb=255*phaseHeat;
  noStroke();
  for (int i=0; i<8; i++) {
    float xp=i*(w/7.0f), fh=random(12, 28)*intensity, fw=random(8, 16), off=random(-3, 3);
    fill(fr, fg, fb, 110);
    ellipse(xp+off, field_top+fh/2, fw, fh);
    ellipse(xp+off, field_bottom-fh/2, fw, fh);
  }
  for (int i=0; i<6; i++) {
    float yp=field_top+i*(field_h/5.0f), fw=random(12, 28)*intensity, fh=random(8, 16), off=random(-3, 3);
    fill(fr, fg, fb, 110);
    ellipse(fw/2, yp+off, fw, fh);
    ellipse(field_w-fw/2, yp+off, fw, fh);
  }
}

void draw_phase4_energy_flow(float phaseHeat) {
  if (phase4_stream_progress.length!=phase4_stream_count) {
    phase4_stream_progress=new float[phase4_stream_count];
    for (int i=0; i<phase4_stream_count; i++)phase4_stream_progress[i]=(i*137.0f%1000)/1000.0f;
  }
  float flow=8+phaseHeat*50, length=45+phaseHeat*130, cx=field_w/2.0f, cy=field_top+field_h/2.0f;
  for (int i=0; i<phase4_stream_count; i++) {
    phase4_stream_progress[i]+=flow/1000.0f;
    if (phase4_stream_progress[i]>=1)phase4_stream_progress[i]-=1;
    float sx, sy;
    int side=i%4;
    if (side==0) {
      sx=(i*137)%field_w;
      sy=field_top;
    } else if (side==1) {
      sx=field_w;
      sy=field_top+(i*83)%field_h;
    } else if (side==2) {
      sx=(i*137)%field_w;
      sy=field_bottom;
    } else {
      sx=0;
      sy=field_top+(i*83)%field_h;
    }
    float dx=cx-sx, dy=cy-sy, dist=sqrt(dx*dx+dy*dy);
    if (dist==0)continue;
    dx/=dist;
    dy/=dist;
    float travel=phase4_stream_progress[i]*dist, px=sx+dx*travel, py=sy+dy*travel, tx=px-dx*length, ty=py-dy*length;
    float alpha=(90+phaseHeat*150)*constrain(phase4_stream_progress[i]*8, 0, 1)*constrain((1-phase4_stream_progress[i])*8, 0, 1);
    stroke(80, 190, 255, alpha*.45f);
    strokeWeight(3+phaseHeat*3);
    line(tx, ty, px, py);
    stroke(180, 235, 255, alpha);
    strokeWeight(1.5f+phaseHeat*2.5f);
    line(tx, ty, px, py);
  }
  float pulse=(sin(millis()*.015f)+1)/2, intensity=70+pulse*100;
  noFill();
  for (int i=0; i<5; i++) {
    stroke(80, 190+40*phaseHeat, 255, intensity*(1-i/5.0f));
    strokeWeight(3+i*3+phaseHeat*3);
    rect(field_w/2.0f, field_top+field_h/2.0f, field_w-20+i*4, field_h-20+i*4);
  }
  stroke(180, 235, 255, 150+pulse*105);
  strokeWeight(2+phaseHeat*2);
  rect(field_w/2.0f, field_top+field_h/2.0f, field_w-20, field_h-20);
}

void start_phase5() {
  phase5_started=true;
  phase5_burst_start=millis();
  create_phase5_energy();
}

void create_phase5_energy() {
  phase5_stream_progress=new float[phase5_stream_count];
  phase5_stream_angles=new float[phase5_stream_count];
  phase5_stream_colors=new int[phase5_stream_count][];
  phase5_stream_dx=new float[phase5_stream_count];
  phase5_stream_dy=new float[phase5_stream_count];
  phase5_stream_edge_distance=new float[phase5_stream_count];
  for (int i=0; i<phase5_stream_count; i++) {
    phase5_stream_progress[i]=random(1);
    phase5_stream_angles[i]=random(TWO_PI);
    set_phase5_stream_direction(i);
    set_stream_color(i,(int)random(8));
  }
}
void set_phase5_stream_direction(int i) {
  float angle=phase5_stream_angles[i];
  float dx=cos(angle), dy=sin(angle);
  float cx=field_w/2.0f, cy=field_top+field_h/2.0f;
  float distanceX=dx>0 ? (field_w-cx)/dx : dx<0 ? (0-cx)/dx : Float.MAX_VALUE;
  float distanceY=dy>0 ? (field_bottom-cy)/dy : dy<0 ? (field_top-cy)/dy : Float.MAX_VALUE;
  phase5_stream_dx[i]=dx;
  phase5_stream_dy[i]=dy;
  phase5_stream_edge_distance[i]=min(distanceX,distanceY);
}
void set_stream_color(int i,int type) {
  phase5_stream_colors[i]=PHASE5_COLORS[type];
}

void draw_phase5_cosmic_radiation() {
  if (phase5_stream_progress.length!=phase5_stream_count) create_phase5_energy();
  float cx=field_w/2.0f, cy=field_top+field_h/2.0f;
  for(int i=0;i<phase5_stream_count;i++) {
    phase5_stream_progress[i]+=.05f;
    if(phase5_stream_progress[i]>=1) {
      phase5_stream_progress[i]=random(.15f);
      phase5_stream_angles[i]=random(TWO_PI);
      set_phase5_stream_direction(i);
      set_stream_color(i,(int)random(8));
    }
    float progress=phase5_stream_progress[i], dx=phase5_stream_dx[i], dy=phase5_stream_dy[i];
    float distance=phase5_stream_edge_distance[i];
    float px=cx+dx*progress*distance, py=cy+dy*progress*distance;
    float len=100+random(30), tx=px-dx*len, ty=py-dy*len;
    float alpha=255*constrain(progress*10,0,1)*constrain((1-progress)*8,0,1);
    int[] c=phase5_stream_colors[i];
    stroke(c[0],c[1],c[2],alpha*.35f); strokeWeight(10); line(tx,ty,px,py);
    stroke(c[0],c[1],c[2],alpha); strokeWeight(4); line(tx,ty,px,py);
    stroke(255,255,255,alpha*.7f); strokeWeight(1.5f); line(tx,ty,px,py);
  }
}

void draw_phase5_explosion() {
  int elapsed=millis()-phase5_burst_start, duration=700;
  if (elapsed>=duration)return;
  float t=elapsed/(float)duration, alpha=t<.15f?255*(t/.15f):255*(1-(t-.15f)/.85f);
  alpha=constrain(alpha, 0, 255);
  noStroke();
  fill(255, 255, 255, alpha*.85f);
  rectMode(CORNER);
  rect(0, 0, w, h);
  rectMode(CENTER);
  fill(255, 255, 255, alpha*.30f);
  float size=80+t*500;
  ellipse(field_w/2.0f, field_top+field_h/2.0f, size, size);
}

void create_phase5_stars() {
  phase5_stars.clear();
  randomSeed(25);
  for(int i=0;i<80;i++) phase5_stars.add(new Star(random(field_w),random(field_top,field_bottom),random(40,130),random(1,3)));
  phase5_star_layer=createGraphics(w,h);
  phase5_star_layer.beginDraw();
  phase5_star_layer.clear();
  phase5_star_layer.ellipseMode(CENTER);
  phase5_star_layer.noStroke();
  for(Star star:phase5_stars) {
    phase5_star_layer.fill(255,255,255,star.brightness);
    phase5_star_layer.ellipse(star.x,star.y,star.size,star.size);
  }
  phase5_star_layer.endDraw();
}
void draw_phase5_stars() {
  if(phase5_stars.size()==0 || phase5_star_layer==null) create_phase5_stars();
  image(phase5_star_layer,0,0);
}
void draw_phase5_center_glow() {
  float cx=field_w/2.0f, cy=field_top+field_h/2.0f, p=(sin(millis()*.01f)+1)/2;
  noStroke();
  for (int i=0; i<6; i++) {
    fill(150, 80, 255, 25-i*3);
    float z=80+i*35+p*20;
    ellipse(cx, cy, z, z);
  }
  for (int i=0; i<4; i++) {
    fill(220, 230, 255, 40-i*7);
    float z=45+i*18+p*10;
    ellipse(cx, cy, z, z);
  }
  fill(255);
  ellipse(cx, cy, 25+p*5, 25+p*5);
}
void draw_phase5_cosmic_frame() {
  float p=(sin(millis()*.012f)+1)/2;
  noFill();
  for (int i=0; i<5; i++) {
    stroke(150, 80, 255, 45-i*7);
    strokeWeight(3+i*3);
    rect(field_w/2.0f, field_top+field_h/2.0f, field_w-20+i*5, field_h-20+i*5);
  }
  stroke(230, 230, 255, 150+p*100);
  strokeWeight(2);
  rect(field_w/2.0f, field_top+field_h/2.0f, field_w-20, field_h-20);
}

void create_hit_particles(float hx, float hy, String direction) {
  for (int i=0; i<10; i++) {
    float spread=random(-PI/3, PI/3), angle=direction.equals("left")?spread:PI+spread, speed=random(2, 5);
    particles.add(new HitParticle(hx, hy, cos(angle)*speed, sin(angle)*speed, millis(), (int)random(100, 200), random(2, 5)));
  }
}
void update_hit_particles() {
  for (int i=particles.size()-1; i>=0; i--) {
    HitParticle p=particles.get(i);
    p.x+=p.vx;
    p.y+=p.vy;
    if (millis()-p.start>=p.life)particles.remove(i);
  }
}
void draw_hit_particles() {
  noStroke();
  for (HitParticle p : particles) {
    float alpha=255*(1-(millis()-p.start)/(float)p.life);
    fill(255, alpha);
    ellipse(p.x, p.y, p.size, p.size);
  }
}
void draw_game_objects() {
  draw_ball();
  draw_ball_trail();
  draw_paddles();
}
void draw_ball() {
  int phase=get_heat_phase();
  noStroke();
  if (phase==1) {
    fill(255);
    ellipse(x, y, radius*2, radius*2);
  } else if (phase==2) {
    float t=constrain((get_heat()-25)/25, 0, 1);
    fill(255, 255-135*t, 255-255*t);
    ellipse(x, y, radius*2, radius*2);
  } else if (phase==3) {
    float t=constrain((get_heat()-50)/25, 0, 1), r=255-255*t, g=120+135*t, b=255*t;
    fill(r, g, b);
    ellipse(x, y, radius*2, radius*2);
    fill(255-255*t, 220+35*t, 120+135*t, 180);
    float speed=max(.001f, get_speed());
    ellipse(x-vx/speed*5, y-vy/speed*5, radius, radius);
  } else if (phase==4) {
    float t=constrain((get_heat()-75)/25, 0, 1);
    fill(40+150*t, 140+100*t, 255, 70);
    float sz=radius*(3.5f+t*1.5f);
    ellipse(x, y, sz, sz);
    fill(120+135*t, 190+65*t, 255);
    ellipse(x, y, radius*2, radius*2);
  } else {
    float p=(sin(millis()*.02f)+1)/2;
    fill(220, 230, 255, 25);
    ellipse(x, y, radius*6+p*8, radius*6+p*8);
    fill(230, 240, 255, 45);
    ellipse(x, y, radius*4+p*5, radius*4+p*5);
    fill(245, 250, 255, 100);
    ellipse(x, y, radius*2.5f, radius*2.5f);
    fill(255);
    ellipse(x, y, radius*1.5f, radius*1.5f);
  }
}
void draw_ball_trail() {
  int phase=get_heat_phase();
  float speed=get_speed();
  if (speed==0)return;
  float dx=vx/speed, dy=vy/speed, no=0;
  if (phase==2) {
    float t=constrain((get_heat()-25)/25, 0, 1), len=10+15*t;
    noStroke();
    fill(255, 120, 0, 60);
    ellipse(x-dx*len, y-dy*len, radius*1.3f, radius*1.3f);
  } else if (phase==3) {
    float t=constrain((get_heat()-50)/25, 0, 1), r=255-255*t, g=120+135*t, b=255*t;
    fill(r, g, b, 45);
    ellipse(x, y, radius*3, radius*3);
    fill(r, g, b);
    ellipse(x, y, radius*2, radius*2);
    fill(255-255*t, 220+35*t, 120+135*t, 170);
    ellipse(x-dx*4, y-dy*4, radius*.8f, radius*.8f);
  } else if (phase==4) {
    float t=constrain((get_heat()-75)/25, 0, 1), len=45+55*t;
    fill(70+130*t, 170+60*t, 255, 70);
    ellipse(x-dx*len, y-dy*len, radius*1.4f, radius*1.4f);
    fill(220, 245, 255, 120);
    ellipse(x-dx*len*.45f, y-dy*len*.45f, radius*.8f, radius*.8f);
  } else if (phase==5) {
    noStroke();
    float len=140;
    for (int i=0; i<8; i++) {
      float t=i/8.0f;
      fill(170, 220, 255, 45*(1-t));
      float z=radius*(2.8f-t*1.8f);
      ellipse(x-dx*len*t, y-dy*len*t, z, z);
    }
    for (int i=0; i<10; i++) {
      float t=i/10.0f;
      fill(220, 240, 255, 110*(1-t));
      float z=radius*(1.5f-t*.9f);
      ellipse(x-dx*len*t, y-dy*len*t, z, z);
    }
    for (int i=0; i<6; i++) {
      float t=i/6.0f;
      fill(255, 255, 255, 210*(1-t));
      float z=radius*(.75f-t*.45f);
      ellipse(x-dx*len*.75f*t, y-dy*len*.75f*t, z, z);
    }
  }
}

public void keyPressed() {
  if (keyCode==87)w_pressed=true;
  if (keyCode==83)s_pressed=true;
  if (keyCode==UP)up_pressed=true;
  if (keyCode==DOWN)down_pressed=true;
}
public void keyReleased() {
  if (keyCode==87)w_pressed=false;
  if (keyCode==83)s_pressed=false;
  if (keyCode==UP)up_pressed=false;
  if (keyCode==DOWN)down_pressed=false;
}


// Phase 5 performance meter: one-second samples plus session average/min/max.
void update_phase5_fps(int phase) {
  if (phase != 5) {
    phase5_fps_measuring = false;
    return;
  }

  int now = millis();
  if (!phase5_fps_measuring) {
    phase5_fps_measuring = true;
    phase5_fps_session_start = now;
    phase5_fps_window_start = now;
    phase5_fps_last_log = now;
    phase5_fps_window_frames = 0;
    phase5_fps_total_frames = 0;
    phase5_fps_samples = 0;
    phase5_fps_current = 0;
    phase5_fps_average = 0;
    phase5_fps_min = Float.MAX_VALUE;
    phase5_fps_max = 0;
  }

  phase5_fps_window_frames++;
  phase5_fps_total_frames++;
  int windowElapsed = now - phase5_fps_window_start;
  if (windowElapsed >= 1000) {
    phase5_fps_current = phase5_fps_window_frames * 1000.0f / windowElapsed;
    int sessionElapsed = max(1, now - phase5_fps_session_start);
    phase5_fps_average = phase5_fps_total_frames * 1000.0f / sessionElapsed;
    phase5_fps_min = min(phase5_fps_min, phase5_fps_current);
    phase5_fps_max = max(phase5_fps_max, phase5_fps_current);
    phase5_fps_samples++;
    phase5_fps_window_frames = 0;
    phase5_fps_window_start = now;

    if (now - phase5_fps_last_log >= 3000) {
      println("[Phase 5 FPS] current=" + nf(phase5_fps_current, 0, 1)
        + " avg=" + nf(phase5_fps_average, 0, 1)
        + " min=" + nf(phase5_fps_min, 0, 1)
        + " max=" + nf(phase5_fps_max, 0, 1));
      phase5_fps_last_log = now;
    }
  }
}
