import asyncio
from pynput import mouse
from aiogram import Bot
import threading
import time

class MouseTracker:
    def __init__(self):
        self.listener = None
        self.is_tracking = False
        self.chat_id = None
        self.bot = None
        self.loop = None
        self.last_message_time = 0
        self.message_cooldown = 10  # seconds
        self.message_pending = False 
        self.start_pos = [0, 0]
        self.pixel_threshold = 100

    def on_move(self, x, y):
        distance_x = abs(x - self.start_pos[0])
        distance_y = abs(y - self.start_pos[1])
        current_time = time.time()
        
        if (current_time - self.last_message_time >= self.message_cooldown and 
            not self.message_pending and 
            self.bot and self.chat_id and self.loop
            and distance_x > self.pixel_threshold 
            and distance_y > self.pixel_threshold):
            
            self.message_pending = True
            self.last_message_time = current_time
            
            async def send_message():
                await self.bot.send_message(
                    self.chat_id, 
                    f"Мышь была передвинута! Координаты: ({x}, {y})"
                )
                self.message_pending = False
            
            asyncio.run_coroutine_threadsafe(send_message(), self.loop)

    def start(self, bot: Bot, chat_id: int):
        if not self.is_tracking:
            self.loop = asyncio.get_event_loop()

            with mouse.Controller() as controller:
                x, y = controller.position
                self.start_pos = [x, y]

            self.listener = mouse.Listener(
                on_move=self.on_move,
            )
            self.bot = bot
            self.chat_id = chat_id
            self.last_message_time = 0
            self.message_pending = False
            self.listener.start()
            self.is_tracking = True
            print("Start mouse tracker")
    
    def stop(self):
        if self.is_tracking:
            self.listener.stop()
            self.is_tracking = False
            self.message_pending = False
            print("Stop mouse tracking")

mouse_tracker = MouseTracker()