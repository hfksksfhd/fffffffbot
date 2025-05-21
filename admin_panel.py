import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime


# ايدي الادمن
ADMIN_ID = 6392238598
ADMINS_FILE = 'admins.json'
BANNED_USERS_FILE = 'banned_users.json'
BOT_DATA_FILE = 'bot_data.json'
USERS_FILE = 'users.json'
FORCE_CHANNELS_FILE = 'force_channels.json'


EMOJIS = {
    'admin': '👑',
    'ban': '🚫',
    'unban': '✅',
    'stop': '⛔',
    'start': '▶️',
    'notifications': '🔔',
    'add_admin': '➕',
    'remove_admin': '➖',
    'admins_list': '👥',
    'banned_list': '📋',
    'broadcast': '📢',
    'settings': '⚙️',
    'back': '🔙',
    'warning': '⚠️',
    'success': '✨',
    'error': '❌',
    'info': 'ℹ️',
    'power': '⚡️',
    'notification': '🔔',
    'list': '📝',
    'ban_list': '🚫',
    'add_channel': '📢',
    'remove_channel': '🚫',
    'channels_list': '📝',
    'stats': '📊',
    'users': '👥',
    'messages': '📨',
    'time': '🕰️',
    'status': '🔋',
    'user': '👤',
}

class AdminPanel:
    def __init__(self, bot):
        self.bot = bot
        self.admins = []
        self.banned_users = []
        self.notifications_enabled = True
        self.bot_data = {'is_active': True, 'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        self.users_data = {'users': []}
        self.force_channels = []  



        self.load_admins()
        self.load_banned_users()
        self.load_bot_data()
        self.load_users_data()
        self.load_force_channels()

    def load_admins(self):


        if os.path.exists(ADMINS_FILE):
            with open(ADMINS_FILE, 'r') as f:
                self.admins = json.load(f)
        else:
            self.admins = [ADMIN_ID]
            self.save_admins()

    def load_banned_users(self):


        if os.path.exists(BANNED_USERS_FILE):
            with open(BANNED_USERS_FILE, 'r') as f:
                self.banned_users = json.load(f)
        else:
            self.banned_users = []
            self.save_banned_users()

    def load_bot_data(self):


        try:
            with open(BOT_DATA_FILE, 'r', encoding='utf-8') as f:
                self.bot_data = json.load(f)
        except FileNotFoundError:
            self.bot_data = {'is_active': True, 'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            self.save_bot_data()

    def load_users_data(self):

        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                self.users_data = json.load(f)
        except FileNotFoundError:
            self.users_data = {'users': []}
            self.save_users_data()

    def load_force_channels(self):

        try:
            with open(FORCE_CHANNELS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.force_channels = data.get('channels', [])
        except FileNotFoundError:
            self.save_force_channels()

    def save_admins(self):

        with open(ADMINS_FILE, 'w') as f:
            json.dump(self.admins, f)

    def save_banned_users(self):

        with open(BANNED_USERS_FILE, 'w') as f:
            json.dump(self.banned_users, f)

    def save_bot_data(self):

        with open(BOT_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.bot_data, f)

    def save_users_data(self):

        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.users_data, f, ensure_ascii=False, indent=2)

    def save_force_channels(self):

        with open(FORCE_CHANNELS_FILE, 'w', encoding='utf-8') as f:
            json.dump({'channels': self.force_channels}, f, ensure_ascii=False, indent=4)

    def create_admin_keyboard(self):

        keyboard = InlineKeyboardMarkup(row_width=2)
        

        main_buttons = [
            (f"{EMOJIS['broadcast']} إذاعة", 'admin_broadcast'),
            (f"{EMOJIS['notification']} {'إيقاف' if self.notifications_enabled else 'تشغيل'} الإشعارات", 'admin_toggle_notifications'),
            (f"{EMOJIS['power']} {'إيقاف' if self.bot_data['is_active'] else 'تشغيل'} البوت", 'admin_toggle_bot'),
            (f"{EMOJIS['stats']} إحصائيات كاملة", 'admin_full_stats'),
        ]
        

        user_buttons = [
            (f"{EMOJIS['ban']} حظر مستخدم", 'admin_ban'),
            (f"{EMOJIS['unban']} فك حظر مستخدم", 'admin_unban'),
        ]
        

        admin_buttons = [
            (f"{EMOJIS['add_admin']} إضافة مشرف", 'admin_add'),
            (f"{EMOJIS['remove_admin']} إزالة مشرف", 'admin_remove'),
        ]
        

        list_buttons = [
            (f"{EMOJIS['list']} قائمة المشرفين", 'admin_list_admins'),
            (f"{EMOJIS['ban_list']} قائمة المحظورين", 'admin_list_banned'),
        ]
        

        force_sub_buttons = [
            (f"{EMOJIS['add_channel']} إضافة قناة اشتراك", 'admin_add_channel'),
            (f"{EMOJIS['remove_channel']} إزالة قناة اشتراك", 'admin_remove_channel'),
            (f"{EMOJIS['channels_list']} قنوات الاشتراك", 'admin_list_channels'),
        ]
        

        for text, callback in main_buttons:
            keyboard.add(InlineKeyboardButton(text, callback_data=callback))
        
        keyboard.row(
            *[InlineKeyboardButton(text, callback_data=callback) for text, callback in user_buttons]
        )
        
        keyboard.row(
            *[InlineKeyboardButton(text, callback_data=callback) for text, callback in admin_buttons]
        )
        
        keyboard.row(
            *[InlineKeyboardButton(text, callback_data=callback) for text, callback in list_buttons]
        )
        

        for text, callback in force_sub_buttons:
            keyboard.add(InlineKeyboardButton(text, callback_data=callback))
        
        return keyboard

    def handle_admin_command(self, message):

        if not self.is_admin(message.from_user.id):
            self.bot.reply_to(
                message,
                f"{EMOJIS['error']} عذراً، هذا الأمر للمشرفين فقط"
            )
            return
            

        admin_message = (
            f"{EMOJIS['admin']} لوحة تحكم المشرفين\n\n"
            f"{EMOJIS['info']} معلومات البوت:\n"
            f"├ {EMOJIS['power']} الحالة: {'يعمل' if self.bot_data['is_active'] else 'متوقف'}\n"
            f"├ {EMOJIS['notification']} الإشعارات: {'مفعلة' if self.notifications_enabled else 'معطلة'}\n"
            f"├ {EMOJIS['list']} عدد المشرفين: {len(self.admins)}\n"
            f"└ {EMOJIS['ban_list']} عدد المحظورين: {len(self.banned_users)}\n\n"
            f"{EMOJIS['info']} اختر أحد الخيارات :"
        )
        
        self.bot.reply_to(
            message,
            admin_message,
            reply_markup=self.create_admin_keyboard()
        )

    def is_admin(self, user_id):

        return user_id in self.admins

    def is_banned(self, user_id):

        return user_id in self.banned_users

    def handle_admin_callback(self, call):

        if not self.is_admin(call.from_user.id):
            self.bot.answer_callback_query(
                call.id,
                f"{EMOJIS['error']} عذراً، هذا الأمر للمشرفين فقط",
                show_alert=True
            )
            return

        action = call.data.replace('admin_', '')
        
        if action == 'ban':
            msg = self.bot.edit_message_text(
                f"{EMOJIS['ban']} أدخل معرف المستخدم المراد حظره:",
                call.message.chat.id,
                call.message.message_id
            )
            self.bot.register_next_step_handler(msg, self.handle_ban_user)
            
        elif action == 'unban':
            msg = self.bot.edit_message_text(
                f"{EMOJIS['unban']} أدخل معرف المستخدم المراد فك حظره:",
                call.message.chat.id,
                call.message.message_id
            )
            self.bot.register_next_step_handler(msg, self.handle_unban_user)
            
        elif action == 'toggle_bot':

            self.bot_data['is_active'] = not self.bot_data['is_active']
            self.save_bot_data()
            
            status = "تشغيل" if self.bot_data['is_active'] else "إيقاف"
            self.bot.answer_callback_query(
                call.id,
                f"{EMOJIS['success']} تم {status} البوت بنجاح!",
                show_alert=True
            )
            

            admin_message = (
                f"{EMOJIS['admin']} لوحة تحكم المشرفين\n\n"
                f"{EMOJIS['info']} معلومات البوت:\n"
                f"├ {EMOJIS['power']} الحالة: {'يعمل' if self.bot_data['is_active'] else 'متوقف'}\n"
                f"├ {EMOJIS['notification']} الإشعارات: {'مفعلة' if self.notifications_enabled else 'معطلة'}\n"
                f"├ {EMOJIS['list']} عدد المشرفين: {len(self.admins)}\n"
                f"└ {EMOJIS['ban_list']} عدد المحظورين: {len(self.banned_users)}\n\n"
                f"{EMOJIS['info']} اختر أحد الخيارات أدناه:"
            )
            
            self.bot.edit_message_text(
                admin_message,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=self.create_admin_keyboard()
            )
            
        elif action == 'toggle_notifications':

            self.notifications_enabled = not self.notifications_enabled
            
            status = "تشغيل" if self.notifications_enabled else "إيقاف"
            self.bot.answer_callback_query(
                call.id,
                f"{EMOJIS['success']} تم {status} الإشعارات بنجاح!",
                show_alert=True
            )


            admin_message = (
                f"{EMOJIS['admin']} لوحة تحكم المشرفين\n\n"
                f"{EMOJIS['info']} معلومات البوت:\n"
                f"├ {EMOJIS['power']} الحالة: {'يعمل' if self.bot_data['is_active'] else 'متوقف'}\n"
                f"├ {EMOJIS['notification']} الإشعارات: {'مفعلة' if self.notifications_enabled else 'معطلة'}\n"
                f"├ {EMOJIS['list']} عدد المشرفين: {len(self.admins)}\n"
                f"└ {EMOJIS['ban_list']} عدد المحظورين: {len(self.banned_users)}\n\n"
                f"{EMOJIS['info']} اختر أحد الخيارات :"
            )
            
            self.bot.edit_message_text(
                admin_message,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=self.create_admin_keyboard()
            )
            
        elif action == 'add':
            msg = self.bot.edit_message_text(
                f"{EMOJIS['add_admin']} أدخل معرف المستخدم لإضافته كمشرف:",
                call.message.chat.id,
                call.message.message_id
            )
            self.bot.register_next_step_handler(msg, self.add_admin)
            
        elif action == 'remove':
            msg = self.bot.edit_message_text(
                f"{EMOJIS['remove_admin']} أدخل معرف المستخدم لإزالته من المشرفين:",
                call.message.chat.id,
                call.message.message_id
            )
            self.bot.register_next_step_handler(msg, self.remove_admin)
            
        elif action == 'list_admins':

            admins_text = f"{EMOJIS['list']} قائمة المشرفين:\n\n"
            
            for admin_id in self.admins:

                admin = None
                for user in self.users_data['users']:
                    if user['id'] == admin_id:
                        admin = user
                        break
                        
                if admin:
                    admins_text += f"├ {EMOJIS['info']} المعرف: @{admin['username']}\n"
                    admins_text += f"├ {EMOJIS['info']} الآيدي: {admin_id}\n"
                    admins_text += f"└ {EMOJIS['info']} تاريخ الانضمام: {admin['joined_date']}\n\n"
                else:
                    admins_text += f"├ {EMOJIS['info']} الآيدي: {admin_id}\n"
                    admins_text += f"└ {EMOJIS['warning']} معلومات غير متوفرة\n\n"
                    
            self.bot.edit_message_text(
                admins_text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=self.create_back_keyboard()
            )
            
        elif action == 'list_banned':

            banned_text = f"{EMOJIS['ban_list']} قائمة المحظورين:\n\n"
            
            for banned_id in self.banned_users:

                banned = None
                for user in self.users_data['users']:
                    if user['id'] == banned_id:
                        banned = user
                        break
                        
                if banned:
                    banned_text += f"├ {EMOJIS['info']} المعرف: @{banned['username']}\n"
                    banned_text += f"├ {EMOJIS['info']} الآيدي: {banned_id}\n"
                    banned_text += f"└ {EMOJIS['info']} تاريخ الانضمام: {banned['joined_date']}\n\n"
                else:
                    banned_text += f"├ {EMOJIS['info']} الآيدي: {banned_id}\n"
                    banned_text += f"└ {EMOJIS['warning']} معلومات غير متوفرة\n\n"
                    
            self.bot.edit_message_text(
                banned_text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=self.create_back_keyboard()
            )
            
        elif action == 'broadcast':
            msg = self.bot.edit_message_text(
                f"{EMOJIS['broadcast']} أدخل الرسالة المراد إذاعتها لجميع المستخدمين:",
                call.message.chat.id,
                call.message.message_id
            )
            self.bot.register_next_step_handler(msg, self.broadcast_message)
            
        elif action == 'back':

            admin_message = (
                f"{EMOJIS['admin']} لوحة تحكم المشرفين\n\n"
                f"{EMOJIS['info']} معلومات البوت:\n"
                f"├ {EMOJIS['power']} الحالة: {'يعمل' if self.bot_data['is_active'] else 'متوقف'}\n"
                f"├ {EMOJIS['notification']} الإشعارات: {'مفعلة' if self.notifications_enabled else 'معطلة'}\n"
                f"├ {EMOJIS['list']} عدد المشرفين: {len(self.admins)}\n"
                f"└ {EMOJIS['ban_list']} عدد المحظورين: {len(self.banned_users)}\n\n"
                f"{EMOJIS['info']} اختر أحد الخيارات :"
            )
            
            self.bot.edit_message_text(
                admin_message,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=self.create_admin_keyboard()
            )

        elif action == 'add_channel':
            msg = self.bot.edit_message_text(
                f"{EMOJIS['add_channel']} أدخل معرف القناة لإضافتها للاشتراك الإجباري:\n"
                f"مثال: @channel",
                call.message.chat.id,
                call.message.message_id
            )
            self.bot.register_next_step_handler(msg, self.add_force_channel)
            
        elif action == 'remove_channel':
            if not self.force_channels:
                self.bot.answer_callback_query(
                    call.id,
                    f"{EMOJIS['error']} لا توجد قنوات اشتراك إجباري",
                    show_alert=True
                )
                return
                
            msg = self.bot.edit_message_text(
                f"{EMOJIS['remove_channel']} أدخل معرف القناة لإزالتها من الاشتراك الإجباري:",
                call.message.chat.id,
                call.message.message_id
            )
            self.bot.register_next_step_handler(msg, self.remove_force_channel)
            
        elif action == 'list_channels':
            channels_text = f"{EMOJIS['channels_list']} قنوات الاشتراك الإجباري:\n\n"
            
            if not self.force_channels:
                channels_text += f"{EMOJIS['info']} لا توجد قنوات اشتراك إجباري"
            else:
                for channel in self.force_channels:
                    try:
                        chat = self.bot.get_chat(channel)
                        channels_text += f"├ {EMOJIS['info']} المعرف: {channel}\n"
                        channels_text += f"├ {EMOJIS['info']} الاسم: {chat.title}\n"
                        channels_text += f"└ {EMOJIS['info']} النوع: {chat.type}\n\n"
                    except:
                        channels_text += f"├ {EMOJIS['info']} المعرف: {channel}\n"
                        channels_text += f"└ {EMOJIS['warning']} لا يمكن الوصول للقناة\n\n"
                        
            self.bot.edit_message_text(
                channels_text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=self.create_back_keyboard()
            )

        elif action == 'full_stats':

            stats_text = self.get_full_stats()
            
            self.bot.edit_message_text(
                stats_text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=self.create_back_keyboard()
            )

    def create_back_keyboard(self):

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(
            f"{EMOJIS['back']} رجوع للوحة التحكم",
            callback_data='admin_back'
        ))
        return keyboard

    def get_user_by_username(self, username):


        username = username.replace('@', '')
        
        for user in self.users_data['users']:
            if user['username'] and user['username'].lower() == username.lower():
                return user
        return None

    def get_user_by_id(self, user_id):

        try:
            user_id = int(user_id)
            for user in self.users_data['users']:
                if user['id'] == user_id:
                    return user
        except ValueError:
            pass
        return None

    def handle_ban_user(self, message):

        try:
            user_input = message.text.strip()
            

            user = None
            if user_input.startswith('@'):

                user = self.get_user_by_username(user_input)
            else:

                user = self.get_user_by_id(user_input)
                
            if not user:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} لم يتم العثور على المستخدم\n\n"
                    f"{EMOJIS['info']} يمكنك إدخال:\n"
                    f"├ معرف المستخدم مثل: @username\n"
                    f"└ آيدي المستخدم مثل: 123456789"
                )
                return
                
            user_id = user['id']
            

            if self.is_admin(user_id):
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} لا يمكن حظر المشرفين"
                )
                return
                
            if user_id == ADMIN_ID:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} لا يمكن حظر المشرف الرئيسي"
                )
                return
                
            if self.is_banned(user_id):
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} هذا المستخدم محظور بالفعل"
                )
                return
                

            self.banned_users.append(user_id)
            self.save_banned_users()
            

            ban_message = (
                f"{EMOJIS['success']} تم حظر المستخدم بنجاح\n\n"
                f"{EMOJIS['info']} معلومات المستخدم:\n"
                f"├ {EMOJIS['info']} المعرف: @{user['username']}\n"
                f"├ {EMOJIS['info']} الآيدي: {user_id}\n"
                f"└ {EMOJIS['info']} تاريخ الانضمام: {user['joined_date']}"
            )
            
            self.bot.reply_to(
                message,
                ban_message,
                reply_markup=self.create_admin_keyboard()
            )
            

            try:
                self.bot.send_message(
                    user_id,
                    f"{EMOJIS['ban']} تم حظرك من استخدام البوت\n"
                    f"{EMOJIS['info']} إذا كنت تعتقد أن هذا خطأ، تواصل مع المشرف."
                )
            except:
                pass
                
        except Exception as e:
            self.bot.reply_to(
                message,
                f"{EMOJIS['error']} حدث خطأ أثناء الحظر\n"
                f"{EMOJIS['info']} الرجاء المحاولة مرة أخرى"
            )
            print(f"خطأ في حظر المستخدم: {str(e)}")

    def handle_unban_user(self, message):

        try:
            user_input = message.text.strip()
            

            user = None
            if user_input.startswith('@'):

                user = self.get_user_by_username(user_input)
            else:

                user = self.get_user_by_id(user_input)
                
            if not user:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} لم يتم العثور على المستخدم\n\n"
                    f"{EMOJIS['info']} يمكنك إدخال:\n"
                    f"├ معرف المستخدم مثل: @username\n"
                    f"└ آيدي المستخدم مثل: 123456789"
                )
                return
                
            user_id = user['id']
            
            if not self.is_banned(user_id):
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} هذا المستخدم غير محظور"
                )
                return
                

            self.banned_users.remove(user_id)
            self.save_banned_users()
            

            unban_message = (
                f"{EMOJIS['success']} تم إلغاء حظر المستخدم بنجاح\n\n"
                f"{EMOJIS['info']} معلومات المستخدم:\n"
                f"├ {EMOJIS['info']} المعرف: @{user['username']}\n"
                f"├ {EMOJIS['info']} الآيدي: {user_id}\n"
                f"└ {EMOJIS['info']} تاريخ الانضمام: {user['joined_date']}"
            )
            
            self.bot.reply_to(
                message,
                unban_message,
                reply_markup=self.create_admin_keyboard()
            )
            

            try:
                self.bot.send_message(
                    user_id,
                    f"{EMOJIS['success']} تم إلغاء حظرك من البوت\n"
                    f"{EMOJIS['info']} يمكنك الآن استخدام البوت بشكل طبيعي."
                )
            except:
                pass
                
        except Exception as e:
            self.bot.reply_to(
                message,
                f"{EMOJIS['error']} حدث خطأ أثناء إلغاء الحظر\n"
                f"{EMOJIS['info']} الرجاء المحاولة مرة أخرى"
            )
            print(f"خطأ في إلغاء حظر المستخدم: {str(e)}")

    def add_user(self, user_id, username):

        users = self.users_data['users']
        if not any(user['id'] == user_id for user in users):
            users.append({
                'id': user_id,
                'username': username,
                'joined_date': str(datetime.now())
            })
            self.save_users_data()

    def get_all_users(self):

        return [user['id'] for user in self.users_data['users']]

    def broadcast_message(self, message):

        message_text = message.text
        success, failed = self.broadcast_message_to_users(message_text)
        
        self.bot.reply_to(
            message,
            f"{EMOJIS['success']} تم إرسال الإذاعة بنجاح\n\n"
            f"{EMOJIS['info']} إحصائيات الإرسال:\n"
            f"├ {EMOJIS['success']} نجح: {success}\n"
            f"└ {EMOJIS['error']} فشل: {failed}",
            reply_markup=self.create_admin_keyboard()
        )

    def broadcast_message_to_users(self, message_text):

        success = 0
        failed = 0
        users = self.get_all_users()
        
        for user_id in users:
            try:
                self.bot.send_message(
                    user_id,
                    f"{EMOJIS['broadcast']} \n{message_text}"
                )
                success += 1
            except Exception as e:
                failed += 1
                print(f"فشل إرسال الإذاعة للمستخدم {user_id}: {str(e)}")
                
        return success, failed

    def notify_admins(self, message):

        if not self.notifications_enabled:
            return
            
        notification = (
            f"{EMOJIS['info']} إشعار جديد\n\n"
            f"├ {EMOJIS['info']} المستخدم: {message.from_user.id}\n"
            f"├ {EMOJIS['info']} المعرف: @{message.from_user.username}\n"
            f"└ {EMOJIS['info']} الرسالة: {message.text}"
        )
        
        for admin_id in self.admins:
            try:
                self.bot.send_message(admin_id, notification)
            except:
                continue

    def add_admin(self, message):

        try:
            user_input = message.text.strip()
            

            user = None
            if user_input.startswith('@'):

                user = self.get_user_by_username(user_input)
            else:

                user = self.get_user_by_id(user_input)
                
            if not user:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} لم يتم العثور على المستخدم\n\n"
                    f"{EMOJIS['info']} يمكنك إدخال:\n"
                    f"├ معرف المستخدم مثل: @username\n"
                    f"└ آيدي المستخدم مثل: 123456789"
                )
                return
                
            user_id = user['id']
            

            if user_id in self.admins:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} هذا المستخدم مشرف بالفعل"
                )
                return
                

            self.admins.append(user_id)
            self.save_admins()
            

            admin_message = (
                f"{EMOJIS['success']} تم إضافة المشرف بنجاح\n\n"
                f"{EMOJIS['info']} معلومات المشرف:\n"
                f"├ {EMOJIS['info']} المعرف: @{user['username']}\n"
                f"├ {EMOJIS['info']} الآيدي: {user_id}\n"
                f"└ {EMOJIS['info']} تاريخ الانضمام: {user['joined_date']}"
            )
            
            self.bot.reply_to(
                message,
                admin_message,
                reply_markup=self.create_admin_keyboard()
            )
            

            try:
                self.bot.send_message(
                    user_id,
                    f"{EMOJIS['success']} تمت ترقيتك كمشرف في البوت\n"
                    f"{EMOJIS['info']} يمكنك الآن استخدام لوحة التحكم عبر /adm"
                )
            except:
                pass
                
        except Exception as e:
            self.bot.reply_to(
                message,
                f"{EMOJIS['error']} حدث خطأ أثناء إضافة المشرف\n"
                f"{EMOJIS['info']} الرجاء المحاولة مرة أخرى"
            )
            print(f"خطأ في إضافة المشرف: {str(e)}")

    def remove_admin(self, message):

        try:
            user_input = message.text.strip()
            

            user = None
            if user_input.startswith('@'):

                user = self.get_user_by_username(user_input)
            else:

                user = self.get_user_by_id(user_input)
                
            if not user:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} لم يتم العثور على المستخدم\n\n"
                    f"{EMOJIS['info']} يمكنك إدخال:\n"
                    f"├ معرف المستخدم مثل: @username\n"
                    f"└ آيدي المستخدم مثل: 123456789"
                )
                return
                
            user_id = user['id']
            
            if user_id == ADMIN_ID:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} لا يمكن إزالة المشرف الرئيسي"
                )
                return
                

            if user_id not in self.admins:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} هذا المستخدم ليس مشرفاً"
                )
                return
                
            self.admins.remove(user_id)
            self.save_admins()
            

            admin_message = (
                f"{EMOJIS['success']} تم إزالة المشرف بنجاح\n\n"
                f"{EMOJIS['info']} معلومات المستخدم:\n"
                f"├ {EMOJIS['info']} المعرف: @{user['username']}\n"
                f"├ {EMOJIS['info']} الآيدي: {user_id}\n"
                f"└ {EMOJIS['info']} تاريخ الانضمام: {user['joined_date']}"
            )
            
            self.bot.reply_to(
                message,
                admin_message,
                reply_markup=self.create_admin_keyboard()
            )
            

            try:
                self.bot.send_message(
                    user_id,
                    f"{EMOJIS['info']} تمت إزالتك من قائمة المشرفين"
                )
            except:
                pass
                
        except Exception as e:
            self.bot.reply_to(
                message,
                f"{EMOJIS['error']} حدث خطأ أثناء إزالة المشرف\n"
                f"{EMOJIS['info']} الرجاء المحاولة مرة أخرى"
            )
            print(f"خطأ في إزالة المشرف: {str(e)}")

    def add_force_channel(self, message):

        try:
            channel = message.text.strip()
            

            if not channel.startswith('@'):
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} عذراً، يجب أن يبدأ معرف القناة بـ @"
                )
                return
                

            try:
                chat = self.bot.get_chat(channel)
            except:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} عذراً، لم يتم العثور على القناة"
                )
                return
                

            try:
                member = self.bot.get_chat_member(chat.id, self.bot.get_me().id)
                if member.status not in ['administrator', 'creator']:
                    self.bot.reply_to(
                        message,
                        f"{EMOJIS['error']} عذراً، يجب أن يكون البوت مشرف في القناة"
                    )
                    return
            except:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} عذراً، لا يمكن التحقق من صلاحيات البوت"
                )
                return
                

            if channel in self.force_channels:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} هذه القناة موجودة بالفعل في الاشتراك الإجباري"
                )
                return
                

            self.force_channels.append(channel)
            self.save_force_channels()
            
            self.bot.reply_to(
                message,
                f"{EMOJIS['success']} تم إضافة القناة للاشتراك الإجباري بنجاح\n\n"
                f"{EMOJIS['info']} معلومات القناة:\n"
                f"├ {EMOJIS['info']} المعرف: {channel}\n"
                f"├ {EMOJIS['info']} الاسم: {chat.title}\n"
                f"└ {EMOJIS['info']} النوع: {chat.type}",
                reply_markup=self.create_admin_keyboard()
            )
            
        except Exception as e:
            self.bot.reply_to(
                message,
                f"{EMOJIS['error']} حدث خطأ أثناء إضافة القناة\n"
                f"{EMOJIS['info']} الرجاء المحاولة مرة أخرى"
            )
            print(f"خطأ في إضافة القناة: {str(e)}")

    def remove_force_channel(self, message):

        try:
            channel = message.text.strip()
            

            if channel not in self.force_channels:
                self.bot.reply_to(
                    message,
                    f"{EMOJIS['error']} عذراً، هذه القناة غير موجودة في الاشتراك الإجباري"
                )
                return
                

            self.force_channels.remove(channel)
            self.save_force_channels()
            
            self.bot.reply_to(
                message,
                f"{EMOJIS['success']} تم إزالة القناة من الاشتراك الإجباري بنجاح",
                reply_markup=self.create_admin_keyboard()
            )
            
        except Exception as e:
            self.bot.reply_to(
                message,
                f"{EMOJIS['error']} حدث خطأ أثناء إزالة القناة\n"
                f"{EMOJIS['info']} الرجاء المحاولة مرة أخرى"
            )
            print(f"خطأ في إزالة القناة: {str(e)}")

    def check_force_subscription(self, user_id):

        if not self.force_channels:
            return [] 
            
        
        not_subscribed = []
        
        for channel in self.force_channels:
            try:
                member = self.bot.get_chat_member(channel, user_id)
                if member.status in ['left', 'kicked']:
                    not_subscribed.append(channel)
            except Exception as e:
                print(f"خطأ في التحقق من اشتراك {user_id} في {channel}: {str(e)}")
                continue
            
        return not_subscribed

    def get_bot_uptime(self):

        start_time = self.bot_data.get('start_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        start_datetime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        uptime = now - start_datetime
        
        days = uptime.days
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        
        uptime_text = ""
        if days > 0:
            uptime_text += f"{days} يوم "
        if hours > 0:
            uptime_text += f"{hours} ساعة "
        if minutes > 0:
            uptime_text += f"{minutes} دقيقة"
        
        return uptime_text.strip() or "أقل من دقيقة"

    def get_messages_today(self):
        today = datetime.now().strftime('%Y-%m-%d')
        return self.bot_data.get('messages_today', {}).get(today, 0)

    def get_banned_users(self):

        banned_users = []
        for user in self.users_data['users']:
            if user.get('banned', False):
                banned_users.append(user)
        return banned_users

    def get_full_stats(self):

        total_users = len(self.users_data['users'])
        messages_today = self.get_messages_today()
        banned_users = self.get_banned_users()
        uptime = self.get_bot_uptime()
        
        banned_users_text = "\n".join([
            f"├ {EMOJIS['user']} @{user.get('username', 'غير معروف')} - {user.get('id')}"
            for user in banned_users
        ]) or "├ لا يوجد مستخدمين محظورين"
        
        stats_text = (
            f"{EMOJIS['stats']} إحصائيات كاملة للبوت:\n\n"
            f"{EMOJIS['users']} عدد المستخدمين: {total_users}\n\n"
            f"{EMOJIS['messages']} الرسائل المستلمة اليوم: {messages_today}\n\n"
            f"{EMOJIS['ban']} المستخدمين المحظورين:\n"
            f"{banned_users_text}\n\n"
            f"{EMOJIS['time']} مدة تشغيل البوت: {uptime}\n\n"
            f"{EMOJIS['status']} حالة البوت: "
            f"{'قيد العمل ✅' if self.bot_data['is_active'] else 'متوقف ❌'}\n"
            f"{EMOJIS['notification']} حالة الإشعارات: "
            f"{'مفتوحة ✅' if self.notifications_enabled else 'مغلقة ❌'}"
        )
        
        return stats_text
