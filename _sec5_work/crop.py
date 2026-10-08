from PIL import Image
src = r"C:\Users\Administrator\Doubao\chats\2026-10-06\new-chat-1\技术栈详解\07_后端开发\_shots\06_MyBatis持久层【深入】_desktop.jpg"
im = Image.open(src)
w, h = im.size
print("size", w, h)
c = im.crop((0, int(h*0.55), w, int(h*0.80)))
out = r"C:\Users\Administrator\Doubao\chats\2026-10-06\new-chat-1\技术栈详解\_sec5_work\mybatis_sec5.jpg"
c.save(out, quality=80)
print("saved", out)
