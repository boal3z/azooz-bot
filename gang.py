import discord
from discord.ext import commands
from discord import ui

# --- إعدادات البوت ---
TOKEN = "MTQ3NjEwNjYwNzMwODk2MzkzMA.GY7TYi.KmS70uTv5CSn58_Kd04buIWfY16t8aa37Pcs1s"

# اسم رتبة المانجر التي لها صلاحية استخدام !setup
ADMIN_ROLE_NAME = "☠️〡𝐆𝐚𝐧𝐠 𝐌𝐀𝐍𝐆𝐄𝐑"

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# --- وظيفة التحقق من رتبة المانجر ---
def is_manager(interaction: discord.Interaction):
    return any(role.name == ADMIN_ROLE_NAME for role in interaction.user.roles)

# --- 1. لوحة "بوس العصابة" (التي ستظهر في روم العصابة) ---
class GangBossView(ui.View):
    def __init__(self, role_id):
        super().__init__(timeout=None)
        self.role_id = role_id

    @ui.button(label="إضافة عضو للعصابة", style=discord.ButtonStyle.success, emoji="➕")
    async def boss_add_member(self, interaction: discord.Interaction, button: ui.Button):
        modal = ui.Modal(title="منح رتبة العصابة")
        user_input = ui.TextInput(label="آيدي العضو الجديد", placeholder="1460406846606278810")
        modal.add_item(user_input)

        async def on_submit_member(it: discord.Interaction):
            try:
                member = it.guild.get_member(int(user_input.value))
                role = it.guild.get_role(int(self.role_id))
                if member and role:
                    await member.add_roles(role)
                    await it.response.send_message(f"✅ تم منح رتبة **{role.name}** للعضو {member.mention}", ephemeral=True)
                else:
                    await it.response.send_message("❌ فشل: العضو أو الرتبة غير موجودة!", ephemeral=True)
            except:
                await it.response.send_message("❌ حدث خطأ في تنفيذ العملية!", ephemeral=True)
        
        modal.on_submit = on_submit_member
        await interaction.response.send_modal(modal)

# --- 2. النافذة التي تطلب البيانات الثلاثة (تظهر للمانجر) ---
class CreatePanelModal(ui.Modal):
    def __init__(self):
        super().__init__(title="إنشاء لوحة عصابة جديدة")
        
        # الطلبات الثلاثة التي حددتها
        self.room_id = ui.TextInput(label="آيدي الصفحة (الروم)", placeholder="ضع آيدي الروم هنا...")
        self.boss_id = ui.TextInput(label="آيدي البوس", placeholder="ضع آيدي البوس هنا...")
        self.role_id = ui.TextInput(label="آيدي الرتبة", placeholder="ضع آيدي الرتبة هنا...")
        
        self.add_item(self.room_id)
        self.add_item(self.boss_id)
        self.add_item(self.role_id)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            channel = bot.get_channel(int(self.room_id.value))
            boss = interaction.guild.get_member(int(self.boss_id.value))
            role = interaction.guild.get_role(int(self.role_id.value))

            if not channel:
                return await interaction.response.send_message("❌ آيدي الصفحة (الروم) غير صحيح!", ephemeral=True)

            embed = discord.Embed(
                title="🛡️ لوحة التحكم الخاصة بالبوس",
                description=(
                    f"مرحباً {boss.mention if boss else 'يا بوس'}\n\n"
                    f"هذه اللوحة مخصصة لك لإدارة أفراد عصابتك.\n"
                    f"الرتبة التي ستتحكم بها: {role.mention if role else 'غير معروفة'}\n\n"
                    "**التعليمات:**\n"
                    "اضغط على الزر أدناه لمنح الرتبة لأعضاء عصابتك مباشرة."
                ),
                color=0x2b2d31 # لون فخم
            )
            
            await channel.send(content=f"تنبيه: {boss.mention if boss else ''}", embed=embed, view=GangBossView(self.role_id.value))
            await interaction.response.send_message(f"✅ تم إرسال اللوحة بنجاح إلى {channel.mention}", ephemeral=True)
        
        except:
            await interaction.response.send_message("❌ خطأ: تأكد من إدخال أرقام (ID) صحيحة!", ephemeral=True)

# --- 3. اللوحة الأم (نفس شكل الصورة تماماً) ---
class MainPanelView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="إضافة لوحة جديدة", style=discord.ButtonStyle.success)
    async def add(self, interaction: discord.Interaction, button: ui.Button):
        if is_manager(interaction):
            await interaction.response.send_modal(CreatePanelModal())
        else:
            await interaction.response.send_message(f"❌ للمانجر فقط ({ADMIN_ROLE_NAME})", ephemeral=True)

    @ui.button(label="حذف لوحة", style=discord.ButtonStyle.danger)
    async def delete(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("🗑️ خاصية الحذف قيد التطوير...", ephemeral=True)

    @ui.button(label="إدارة لوحة", style=discord.ButtonStyle.primary)
    async def manage(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("⚙️ خاصية الإدارة قيد التطوير...", ephemeral=True)

@bot.command()
async def setup(ctx):
    embed = discord.Embed(
        title="☠️ مركز التحكم الرئيسي - نظام العصابات",
        description=(
            "**مميزات النظام:**\n"
            "• لوحة أساسية - مركز التحكم الرئيسي\n"
            "• لوحات فرعية - لكل فريق لوحة خاصة\n"
            "• إدارة كاملة - للقادة فقط\n"
            "• حماية متقدمة - صلاحيات محددة\n\n"
            "**التعليمات:**\n"
            "1. اضغط على **إضافة لوحة جديدة**.\n"
            "2. ادخل آيدي الصفحة، آيدي البوس، وآيدي الرتبة.\n"
            "3. سيقوم البوت بإرسال لوحة التحكم لروم العصابة فوراً."
        ),
        color=0xff0000
    )
    await ctx.send(embed=embed, view=MainPanelView())

@bot.event
async def on_ready():
    print(f'✅ البوت متصل الآن: {bot.user}')

bot.run(TOKEN)