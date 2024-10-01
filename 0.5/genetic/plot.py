import matplotlib.pyplot as plt
import matplotlib.animation as animation
import queue
import threading
import time

fig, ax = plt.subplots()

x_data = []
y_data = []

line, = ax.plot([], [], lw=2)

ax.set_xlabel('Data Point Index')
ax.set_ylabel('Value')

data_queue = queue.Queue()

def data_generator(file_path):
    count = 0
    with open(file_path, 'r') as file:
        for line in file:
            count += 1
            data_queue.put((int(count), float(line)))
        file.seek(0, 2)

        while True:
            line = file.readline()
            if not line:
                continue
            
            count += 1
            try:
                data_queue.put((count, float(line.strip())))
            except ValueError:
                pass

threading.Thread(target=data_generator, args=('data',), daemon=True).start()

def init():
    line.set_data([], [])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 20000)
    return line,

def update(frame):
    if not data_queue.empty():
        t, value = data_queue.get()
        x_data.append(t)
        y_data.append(value)

        line.set_data(x_data, y_data)

        num_points = len(x_data)
        tick_interval = max(1, num_points // 10)

        ax.set_xticks(range(0, num_points + 1, tick_interval))
        ax.set_xticklabels(range(0, num_points + 1, tick_interval))

        ax.set_xlim(0, num_points if num_points > 10 else 10)
        ax.set_ylim(0, max(y_data) + 1)

    return line,

ani = animation.FuncAnimation(fig, update, init_func=init, blit=True)

plt.show()
