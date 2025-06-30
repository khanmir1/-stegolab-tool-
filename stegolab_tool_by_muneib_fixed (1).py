
import gradio as gr
import base64
import os
import tempfile

# ---- CONFIG ----
TOOL_PASSWORD = "cyber123"  # Default password
RESET_PIN = "9090"  # Pin required to reset password

# ---- Global Storage ----
current_password = TOOL_PASSWORD

# ---- Decode + Execute Function ----
def decode_and_run(image, password):
    global current_password
    if password != current_password:
        return "❌ Incorrect password. Access denied."

    try:
        # Save uploaded image temporarily
        temp_dir = tempfile.mkdtemp()
        image_path = os.path.join(temp_dir, "uploaded_image.png")
        image.save(image_path)

        # Decode payload from filename (example: base64 encoded python code in filename)
        filename = os.path.basename(image_path)
        payload_b64 = filename.split(".")[0]  # assuming filename like cHJpbnQoIkhlbGxvISIp.png

        decoded_code = base64.b64decode(payload_b64.encode()).decode(errors="ignore")

        # Execute decoded payload - run inside isolated environment (Use only in trusted environment/VM)
        exec_locals = {}
        exec(decoded_code, {}, exec_locals)

        return f"✅ Payload decoded and executed.\n\nCode:\n{decoded_code}"

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ---- Password Reset Function ----
def reset_password(pin, new_pass):
    global current_password
    if pin == RESET_PIN:
        current_password = new_pass
        return "✅ Password has been reset successfully."
    else:
        return "❌ Invalid reset PIN."

# ---- Gradio UI ----
with gr.Blocks() as app:
    gr.Markdown("""
# 🔐 StegoLab X - Private Payload Tool  
### 🔒 Built for Ethical Testing Only  
#### 👨‍💻 Made by **Muneib Mir**
""")

    with gr.Tab("Main Tool"):
        password = gr.Textbox(label="Enter Tool Password", type="password")
        image_input = gr.Image(label="Upload Payload Image")
        output = gr.Textbox(label="Tool Output", lines=15)
        run_btn = gr.Button("Decode and Auto-Run")
        run_btn.click(decode_and_run, inputs=[image_input, password], outputs=output)

    with gr.Tab("Forgot Password"):
        pin_input = gr.Textbox(label="Enter Reset PIN")
        new_pass_input = gr.Textbox(label="New Password", type="password")
        reset_output = gr.Textbox(label="Reset Result")
        reset_btn = gr.Button("Reset Password")
        reset_btn.click(reset_password, inputs=[pin_input, new_pass_input], outputs=reset_output)

app.launch(server_name="0.0.0.0", server_port=10000)
