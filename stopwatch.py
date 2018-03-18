# template for "Stopwatch: The Game"
import simplegui
# define global variables
tenths = 0
on_second = 0
starts_count = 0
stops_count = 0
minutes = 0
seconds = 0
t = 0
status = 0
interval = 100
# define helper function format that converts integer
# counting tenths of seconds into formatted string A:BC.D
def format(t):
    minutes = str(tenths//600)
    t = str(tenths % 10)
    seconds = tenths//10
    if seconds < 10:
        seconds = "0"+str(tenths//10)
    else:
        seconds = str(tenths//10)
    return minutes+":"+seconds+"."+t+'    '+str(on_second)+"/"+str(stops_count)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    global starts_count,status
    if status == 0:
        starts_count += 1
        status = 1
        timer.start()
    
def stop_timer():
    global stops_count,status,on_second
    if status == 1:
        status = 0
        stops_count += 1
        timer.stop()
        if tenths % 10 == 0:
            on_second +=1

def reset_timer():
    global minutes, seconds, status, t, tenths, starts_count,stops_count,on_second
    minutes = 0
    seconds = 0
    t = 0
    on_second = 0
    starts_count = 0
    stops_count = 0
    tenths = 0
    status = 0
    timer.stop()

# define event handler for timer with 0.1 sec interval
def tick():
    global tenths
    tenths += 1

    
def draw(canvas):
    canvas.draw_text(format(t), [70,100], 40, "White")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 300)
# register event handlers
start_button = frame.add_button("Start", start_timer)
stop_button = frame.add_button("Stop", stop_timer)
reset_button = frame.add_button("Reset", reset_timer)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)

# start timer and frame
frame.start()

# remember to review the grading rubric