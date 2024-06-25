from ursina import *
import random

app = Ursina()  # Set fullscreen=False agar tidak otomatis fullscreen saat dijalankan

mouse.visible = False

# membuat kamera
camera.position = (0, 0, -20)

# membuat crosshair
crosshair = Entity(model='circle', parent=camera.ui, scale=0.01, color=color.white)

# membuat bola 
balls = []
for i in range(5):
    ball = Entity(model='sphere', color=color.yellow, scale=0.5, position=(random.uniform(-3, 3), random.uniform(-3, 3), 0), shadow=True)
    balls.append(ball)

ground = Entity(model='quad', scale=20, texture='white_cube', texture_scale=(40,40), color=color.gray)

timer = 60 
timer_text = Text(text=f'Waktu: {timer//60:02d}:{timer%60:02d}', position=(-0.8, 0.4), scale=2, color=color.white)

score = 0
score_text = Text(text=f'Skor: {score}', position=(-0.8, 0.3), scale=2, color=color.yellow)

info_text = Text(text='[Q] Kurangi Sensitivitas 0.1\n[E] Tambah Sensitivitas 0.1\n[R] Kurangi Sensitivitas 0.01\n[T] Tambah Sensitivitas 0.01\n[V] Toggle Bergerak\n[ESC] Jeda\n[Enter] Keluar', position=(-0.77, -0.32), scale=0.8, color=color.white)

pop_bubble = Audio('pop_bubble.mp3', autoplay=False)

# menghapus bola
def remove_ball(ball):
    global score
    ball.disable()
    balls.remove(ball)
    new_ball = Entity(model='sphere', color=color.yellow, scale=0.5, position=(random.uniform(-3, 3), random.uniform(-3, 3), 0), shadow=True)
    balls.append(new_ball)
    score += 1
    score_text.text = f'Skor: {score}'

sensitivity = 0.8
sensitivity_text = Text(text=f'Sensitivitas: {sensitivity}', position=(-0.8, 0.2), scale=1, color=color.white)

paused = True
pause_text = Text(text='PAUSED', origin=(0,0), scale=3, color=color.blue, enabled=True)

ball_movement_enabled = False
ball_directions = [Vec3(random.uniform(-0.03, 0.03), random.uniform(-0.03, 0.03), 0) for _ in balls]
change_direction_times = [random.uniform(1, 3) for _ in balls]
time_since_last_change = [0 for _ in balls]

fullscreen_enabled = False  # Set initial fullscreen status to False

def update():
    global timer, sensitivity, paused, ball_movement_enabled, ball_directions, change_direction_times, time_since_last_change
    if not paused:
        camera.position = lerp(camera.position, Vec3(mouse.position.x * 20, mouse.position.y * 20, -20), sensitivity)
        crosshair.position = (0, 0)
        
        # update timer
        timer -= time.dt
        timer_text.text = f'Waktu: {int(timer)//60:02d}:{int(timer)%60:02d}'
        
        if timer <= 0:
            final_score_popup = Text(text=f'Permainan Selesai!\nSkor Anda: {score}', origin=(0,0), scale=3, color=color.red, background=True, background_color=color.white)
            final_score_popup.enabled = True
            paused = True

        if ball_movement_enabled:
            for i, ball in enumerate(balls):
                ball.position += ball_directions[i]
                time_since_last_change[i] += time.dt
                if time_since_last_change[i] >= change_direction_times[i]:
                    max_movement = random.uniform(0.005, 0.05)  # Mengubah maksimal movement yang ditempuh
                    ball_directions[i] = Vec3(random.uniform(-max_movement, max_movement), random.uniform(-max_movement, max_movement), 0)
                    change_direction_times[i] = random.uniform(1, 3)
                    time_since_last_change[i] = 0

def input(key):
    global sensitivity, paused, ball_movement_enabled, fullscreen_enabled
    if key == 'left mouse down':
        if paused:
            paused = False
            pause_text.enabled = False
            timer_text.enabled = True
            score_text.enabled = True
            info_text.enabled = True
            sensitivity_text.enabled = True
        else:
            for ball in balls:
                if ball.enabled and distance(ball.position, Vec3(mouse.position.x * 20, mouse.position.y * 20, 0)) < ball.scale_x * 0.5:
                    remove_ball(ball)
                    pop_bubble.play()
                    break

    if key == 'q':
        sensitivity = max(0.01, sensitivity - 0.1)
        sensitivity_text.text = f'Sensitivitas: {sensitivity:.2f}'
    if key == 'e':
        sensitivity = min(2.0, sensitivity + 0.1)
        sensitivity_text.text = f'Sensitivitas: {sensitivity:.2f}'
    if key == 'r':
        sensitivity = max(0.01, sensitivity - 0.01)
        sensitivity_text.text = f'Sensitivitas: {sensitivity:.2f}'
    if key == 't':
        sensitivity = min(2.0, sensitivity + 0.01)
        sensitivity_text.text = f'Sensitivitas: {sensitivity:.2f}'

    if key == 'escape':
        paused = not paused
        pause_text.enabled = paused

    if key == 'enter':
        application.quit()

    if key == 'v':
        ball_movement_enabled = not ball_movement_enabled


app.run()
