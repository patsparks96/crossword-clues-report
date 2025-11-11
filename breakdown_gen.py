import matplotlib.pyplot as plt

# --- Configuration ---
sections = [
    {"text": "One doesn't like", "label": "Definition", "color": "#fff2a8"},
    {"text": "shifting earth", "label": "Wordplay", "color": "#87c2f1"},
    {"text": "test content", "label": "Banana", "color": "#e4ee5a"},
]

enumeration = 5
answer = "hater"

fontsize = 18
label_fontsize = 12
line_gap = 0.07
word_gap = 0.001
section_gap = 0.02
arrow_length = 0.1  # short arrow
section_padding = 0.006  # small horizontal padding at start of each section

# --- Setup ---
fig, ax = plt.subplots(figsize=(12, 2))
ax.axis("off")
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
inv = ax.transData.inverted()

x = 0
section_positions = []

# Draw sections
for section in sections:
    words = section["text"].split()
    word_x = x + section_padding  # apply padding here
    word_widths = []

    for w in words:
        ttmp = ax.text(word_x, 0, w, fontsize=fontsize, va='center', ha='left', color='none')
        fig.canvas.draw()
        bbox = ttmp.get_window_extent(renderer=renderer)
        bbox_data = inv.transform(bbox)
        width = bbox_data[1][0] - bbox_data[0][0]
        word_widths.append(width)
        word_x += width + word_gap

    total_width = sum(word_widths) + word_gap * (len(words)-1) + section_padding  # add padding to total width

    rect = plt.Rectangle((x, -0.25), total_width, 0.5, color=section.get("color", "#8b5599"), zorder=-1)
    ax.add_patch(rect)

    # Draw words with padding
    word_x = x + section_padding
    for w, w_width in zip(words, word_widths):
        ax.text(word_x, 0, w, fontsize=fontsize, va='center', ha='left', color='black')
        word_x += w_width + word_gap

    line_y = 0.2 + line_gap
    ax.plot([x, x + total_width], [line_y, line_y], color='black', linewidth=2)
    ax.plot([x, x], [line_y, line_y - line_gap], color='black', linewidth=2)
    ax.plot([x + total_width, x + total_width], [line_y, line_y - line_gap], color='black', linewidth=2)

    ax.text(x + total_width / 2, line_y + 0.05, section["label"],
            ha='center', va='bottom', fontsize=label_fontsize,
            bbox=dict(facecolor='white', edgecolor='none', pad=2))

    section_positions.append((x, total_width))
    x += total_width + section_gap

# Enumeration text
def_x, def_width = section_positions[-1]
enu_start_x = def_x + def_width + 0.02
enum_obj = ax.text(enu_start_x, 0, f"({enumeration})", fontsize=fontsize, va='center', ha='left')
fig.canvas.draw()
bbox_enum = enum_obj.get_window_extent(renderer=renderer)
bbox_data_enum = inv.transform(bbox_enum)
enum_width = bbox_data_enum[1][0] - bbox_data_enum[0][0]

# Arrow starts just after enumeration
arrow_start_x = enu_start_x + enum_width + 0.02
arrow_start_y = 0
arrow_end_x = arrow_start_x + arrow_length
ax.annotate('', xy=(arrow_end_x, arrow_start_y), xytext=(arrow_start_x, arrow_start_y),
            arrowprops=dict(arrowstyle="->", linewidth=2))

# Answer text immediately after arrow
ax.text(arrow_end_x + 0.02, arrow_start_y, answer, fontsize=fontsize, va='center', ha='left', fontweight='bold')

# Adjust limits based on drawn content
ax.set_xlim(-0.1, arrow_end_x + 0.2)
ax.set_ylim(-0.5, 1.2)
plt.tight_layout()
plt.show()
