#!/usr/bin/env python
"""
cm1_w_spectra_animated.py
-------------------------
Plot and animate horizontal power spectra of vertical velocity (w) from multiple
CM1 output netCDF files, averaged over PBL levels, with a reference line at λ = 6Δx
and a vertical line at the maximum PSD. Also tracks the timeline of maximum PSD.

Includes interactive playback controls: Slider, Play/Pause, Prev/Next, and Speed.
Caches computed spectral frames for seamless and instantaneous manual scrubbing.
Can optionally save the primary animation figure as an animated GIF or an MP4 video.

Usage:
    python cm1_w_spectra_animated.py cm1out_000015.nc cm1out_000016.nc cm1out_000017.nc ...
    or using shell globbing:
    python cm1_w_spectra_animated.py cm1out_*.nc

    To save a video and exit immediately without opening GUI windows:
    python cm1_w_spectra_animated.py cm1out_*.nc --save-video output.mp4

    To save an animated GIF and exit immediately:
    python cm1_w_spectra_animated.py cm1out_*.nc --save-video output.gif

Requirements:
    pip install netCDF4 numpy matplotlib scipy pillow
"""

import os
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.widgets import Slider, Button

from spectra_core import (
    extract_sequence_number,
    format_psd_units,
    read_grid_info,
    HorizontalSpectrum,
    compute_frame_psd,
)


class CM1SpectraAnimator:
    def __init__(
        self,
        files,
        var="winterp",
        pbl_bot_km=0.0,
        pbl_top_km=0.84,
        nsmooth=5,
        detrend=True,
        window=True,
    ):
        self.files = files
        self.num_frames = len(files)
        self.var = var
        self.pbl_bot_km = pbl_bot_km
        self.pbl_top_km = pbl_top_km
        self.nsmooth = nsmooth
        self.detrend = detrend

        self.current_idx = 0
        self.playing = False
        self.cache = {}  # Index -> (wavelength_km, psd_smooth, psd_plot, sim_time_s)

        # Playback speeds (timer interval in milliseconds)
        self.speeds = [150, 400, 1000]  # Fast, Medium, Slow
        self.speed_idx = 1  # Default to Medium

        # Arrays to store time series data for Figure 2
        self.all_times_min = np.zeros(self.num_frames)
        self.all_max_wavelengths_m = np.zeros(self.num_frames)

        # 1. Load coordinates and grid properties from the first file to initialize
        print(
            f"Initializing with baseline parameters from: {os.path.basename(self.files[0])}"
        )
        grid = read_grid_info(self.files[0], self.var, self.pbl_bot_km, self.pbl_top_km)
        self.zh = grid.zh
        self.pbl_mask = grid.pbl_mask
        self.pbl_levels = grid.pbl_levels
        self.dx_m = grid.dx_m
        self.ny, self.nx = grid.ny, grid.nx
        self.var_units = grid.var_units
        if abs(grid.dx_m - grid.dy_m) > 0.1:
            print(
                f"WARNING: Grid is not strictly isotropic: Δx={grid.dx_m:.1f} m, Δy={grid.dy_m:.1f} m"
            )

        self.psd_units_str = format_psd_units(self.var_units)

        print(
            f"  Target variable: {self.var} (raw units: {self.var_units} -> PSD units: {self.psd_units_str})"
        )
        print(
            f"  PBL levels: z = {self.zh[self.pbl_levels[0]]:.3f} – {self.zh[self.pbl_levels[-1]]:.3f} km ({len(self.pbl_levels)} levels)"
        )
        print(
            f"  Horizontal grid dimensions: {self.nx} × {self.ny} (Δx = {self.dx_m:.0f} m)"
        )

        # 2. Build window and radial wavenumber bins for the horizontal spectrum
        self.spectrum = HorizontalSpectrum(self.nx, self.ny, self.dx_m, window=window)
        self.k_rad = self.spectrum.k_rad
        self.slope_x = self.spectrum.slope_x
        self.lambda_anchor = self.spectrum.lambda_anchor

    def get_frame_data(self, idx):
        """Loads variable data from disk and computes horizontal spectra, or loads from cache."""
        if idx in self.cache:
            return self.cache[idx]

        fname = self.files[idx]
        print(
            f"Processing and caching frame {idx + 1}/{self.num_frames}: {os.path.basename(fname)} ... ",
            end="",
            flush=True,
        )

        self.cache[idx] = compute_frame_psd(
            fname,
            self.var,
            self.pbl_mask,
            self.spectrum,
            detrend=self.detrend,
            nsmooth=self.nsmooth,
        )
        print("done.")
        return self.cache[idx]

    def build_gui(self, skip_widgets=False):
        """Constructs interactive plot, widgets, and links callbacks."""
        self.fig, self.ax = plt.subplots(figsize=(9, 6.5))

        if not skip_widgets:
            plt.subplots_adjust(bottom=0.28)  # Leave spacious room for controllers
        else:
            plt.subplots_adjust(bottom=0.15)  # Clean aesthetic for static frame export

        # Load initial frame
        wavelength_km, psd_smooth, psd_plot, sim_time_s = self.get_frame_data(0)

        # Plot Dynamic lines
        (self.line_smooth,) = self.ax.loglog(
            wavelength_km, psd_smooth, color="#1f77b4", lw=1.8, label="PSD (PBL mean)"
        )
        (self.line_raw,) = self.ax.loglog(
            wavelength_km, psd_plot, color="#1f77b4", lw=0.6, alpha=0.35, label="_raw"
        )

        # Plot Static Reference guides
        lambda_6dx_km = (6.0 * self.dx_m) / 1000.0
        lambda_nyq_km = (2.0 * self.dx_m) / 1000.0

        self.ax.axvline(
            lambda_6dx_km,
            color="crimson",
            lw=1.2,
            ls="--",
            label=f"$6\\Delta x$ = {lambda_6dx_km * 1000:.0f} m",
        )
        self.ax.axvline(
            lambda_nyq_km,
            color="gray",
            lw=0.8,
            ls=":",
            label=f"$2\\Delta x$ = {lambda_nyq_km * 1000:.0f} m (Nyquist)",
        )

        # Dynamic Max PSD vertical line initialization
        idx_max = np.argmax(psd_smooth)
        lambda_max = wavelength_km[idx_max]
        self.line_max_psd = self.ax.axvline(
            lambda_max,
            color="darkgreen",
            lw=1.5,
            ls="-.",
            label=f"Max PSD = {lambda_max * 1000:.0f} m",
        )

        # -5/3 Kolmogorov Reference slope
        i_ref = np.argmin(np.abs(wavelength_km - self.lambda_anchor))
        psd_ref_data = psd_smooth[i_ref]
        slope_y = psd_ref_data * (self.slope_x / wavelength_km[i_ref]) ** (5.0 / 3.0)

        (self.line_kolmogorov,) = self.ax.loglog(
            self.slope_x,
            slope_y,
            "k--",
            lw=1.2,
            alpha=0.7,
            label="$k^{-5/3}$ reference",
        )

        # Format axes
        self.ax.set_xlabel("Wavelength (km)", fontsize=11)
        self.ax.set_ylabel(
            f"Power Spectral Density ({self.psd_units_str})", fontsize=11
        )
        self.ax.invert_xaxis()  # Large scales on the left
        self.ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda v, _: f"{v:.2g}"))
        self.ax.legend(fontsize=9, framealpha=0.8, loc="lower left")
        self.ax.grid(True, which="both", ls=":", lw=0.5, alpha=0.5)

        # Set titles
        self.title_element = self.ax.set_title(
            self.get_title_text(0, sim_time_s), fontsize=10
        )

        # Pre-populate timeline data points
        print("\nPre-calculating spectral peaks for the timeline dataset...")
        for i in range(self.num_frames):
            wl, psd_s, _, t_s = self.get_frame_data(i)
            self.all_times_min[i] = t_s / 60.0
            self.all_max_wavelengths_m[i] = wl[np.argmax(psd_s)] * 1000.0
        print("Pre-calculation complete.\n")

        # Create Figure 2 (Timeline Figure) - Always built so we can export it at the end
        self.fig2, self.ax2 = plt.subplots(figsize=(7, 4))
        if self.fig2.canvas.manager is not None:
            self.fig2.canvas.manager.set_window_title("Max PSD Timeline")

        self.ax2.plot(
            self.all_times_min,
            self.all_max_wavelengths_m,
            color="darkgreen",
            lw=2,
            marker="o",
            ms=4,
            label="Dominant Scale",
        )
        (self.time_marker,) = self.ax2.plot(
            self.all_times_min[0],
            self.all_max_wavelengths_m[0],
            color="crimson",
            marker="X",
            ms=10,
            label="Current Frame",
        )

        self.ax2.set_xlabel("Simulation Time (min)", fontsize=11)
        self.ax2.set_ylabel("Wavelength of Max PSD (m)", fontsize=11)
        self.ax2.set_title(
            f"Evolution of Peak PBL Spatial Scale ({self.var})", fontsize=11
        )
        self.ax2.grid(True, ls=":", alpha=0.6)
        self.ax2.legend(fontsize=9, loc="upper left")

        # Skip interactive GUI widgets and layout properties when exporting to files headlessly
        if skip_widgets:
            return

        # --- Interactive Widgets GUI Axes ---
        ax_slider = plt.axes([0.15, 0.16, 0.70, 0.03])
        ax_prev = plt.axes([0.15, 0.06, 0.10, 0.045])
        ax_play = plt.axes([0.27, 0.06, 0.15, 0.045])
        ax_next = plt.axes([0.44, 0.06, 0.10, 0.045])
        ax_speed = plt.axes([0.56, 0.06, 0.14, 0.045])

        # Slider init
        self.slider = Slider(
            ax_slider, "Frame", 0, self.num_frames - 1, valinit=0, valfmt="%0.0f"
        )
        self.slider.on_changed(self.on_slider_move)

        # Button controls
        self.btn_prev = Button(ax_prev, "⏮ Prev")
        self.btn_prev.on_clicked(self.on_prev_click)

        self.btn_play = Button(ax_play, "▶ Play")
        self.btn_play.on_clicked(self.on_play_click)

        self.btn_next = Button(ax_next, "Next ⏭")
        self.btn_next.on_clicked(self.on_next_click)

        self.btn_speed = Button(ax_speed, "Speed: Med")
        self.btn_speed.on_clicked(self.on_speed_click)

        # Cache tracker text display
        self.txt_cache = self.fig.text(
            0.72,
            0.082,
            f"Cache: {len(self.cache)}/{self.num_frames}",
            fontsize=8.5,
            color="#555555",
        )

        # Create a GUI update timer
        self.timer = self.fig.canvas.new_timer(interval=self.speeds[self.speed_idx])
        self.timer.add_callback(self.advance_frame_by_timer)

        plt.figure(self.fig.number)

    def get_title_text(self, idx, sim_time_s):
        """Generates structured title text."""
        return (
            f"CM1 Horizontal ${self.var}$ Spectra — ({self.pbl_bot_km:.2f} ≤ z ≤ {self.pbl_top_km:.2f} km)\n"
            f"File: {os.path.basename(self.files[idx])}  |  t = {sim_time_s / 60:.1f} min\n"
            f"Δx = {self.dx_m:.0f} m  |  Grid: {self.nx}×{self.ny}"
        )

    def update_plot(self, idx, update_timeline_marker=True):
        """Forces updating of arrays on plot curves and titles."""
        wavelength_km, psd_smooth, psd_plot, sim_time_s = self.get_frame_data(idx)

        # Set arrays
        self.line_smooth.set_data(wavelength_km, psd_smooth)
        self.line_raw.set_data(wavelength_km, psd_plot)

        # Dynamically position the reference line
        i_ref = np.argmin(np.abs(wavelength_km - self.lambda_anchor))
        psd_ref_data = psd_smooth[i_ref]
        slope_y = psd_ref_data * (self.slope_x / wavelength_km[i_ref]) ** (5.0 / 3.0)
        self.line_kolmogorov.set_data(self.slope_x, slope_y)

        # Dynamically move the Max PSD vertical line
        idx_max = np.argmax(psd_smooth)
        lambda_max = wavelength_km[idx_max]
        self.line_max_psd.set_xdata([lambda_max, lambda_max])
        self.line_max_psd.set_label(f"Max PSD = {lambda_max * 1000:.0f} m")
        self.ax.legend(fontsize=9, framealpha=0.8, loc="lower left")

        # Let Matplotlib dynamically autoscale y-limits
        self.ax.relim()
        self.ax.autoscale_view(scalex=False, scaley=True)

        # Refresh titles and labels
        self.title_element.set_text(self.get_title_text(idx, sim_time_s))

        if update_timeline_marker:
            if hasattr(self, "txt_cache"):
                self.txt_cache.set_text(f"Cache: {len(self.cache)}/{self.num_frames}")
            current_time_min = sim_time_s / 60.0
            current_max_wl_m = self.all_max_wavelengths_m[idx]
            self.time_marker.set_data([current_time_min], [current_max_wl_m])
            if hasattr(self, "fig2") and self.fig2.canvas is not None:
                self.fig2.canvas.draw_idle()

        self.fig.canvas.draw_idle()

    def save_animation_mp4(self, output_filename, fps=5):
        """
        Compiles all frames into a highly compressed MP4 video using Matplotlib's
        Animation framework and FFmpeg. This utilizes Constant Rate Factor (CRF)
        encoding for minimal file sizes while keeping vector line plots extremely sharp.
        """
        from matplotlib.animation import FFMpegWriter

        print(f"\nGenerating highly compressed MP4 video: {output_filename}")

        # Uses CRF 22 and slow preset to squeeze maximum mathematical compression
        # out of the H.264 codec while preserving pixel-perfect line boundaries.
        writer = FFMpegWriter(
            fps=fps,
            extra_args=[
                "-vcodec",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-crf",
                "22",
                "-preset",
                "slower",
            ],
        )

        with writer.saving(self.fig, output_filename, dpi=120):
            for idx in range(self.num_frames):
                print(f"Writing frame {idx + 1}/{self.num_frames} to video...")
                self.update_plot(idx, update_timeline_marker=False)
                writer.grab_frame()

        print(f"Success! Compressed MP4 saved to: {output_filename}\n")

    def save_animation_gif(self, output_filename, fps=5):
        """
        Renders every active frame sequentially to memory buffers and compiles
        them into an animated GIF using Pillow. Recommended for short animations.
        """
        import io
        from PIL import Image

        print(f"\nGenerating animated GIF: {output_filename}")
        frames = []

        for idx in range(self.num_frames):
            print(f"Rendering frame {idx + 1}/{self.num_frames} into memory...")
            self.update_plot(idx, update_timeline_marker=False)

            buf = io.BytesIO()
            self.fig.savefig(buf, format="png", dpi=120)
            buf.seek(0)
            frames.append(Image.open(buf))

        print("Compiling in-memory structures into an animated GIF file...")
        duration_ms = int(1000 / fps)
        frames[0].save(
            output_filename,
            save_all=True,
            append_images=frames[1:],
            duration=duration_ms,
            loop=0,
        )
        print(f"Success! Animated GIF saved to: {output_filename}\n")

    def save_animation(self, output_filename, fps=5):
        """Routes saving call to specific format based on file extension and saves final timeline plot."""
        ext = os.path.splitext(output_filename)[1].lower()
        if ext == ".gif":
            self.save_animation_gif(output_filename, fps=fps)
        elif ext == ".mp4":
            self.save_animation_mp4(output_filename, fps=fps)
        else:
            print(
                f"Warning: Extension '{ext}' not directly recognized. Defaulting to MP4 video format."
            )
            self.save_animation_mp4(output_filename, fps=fps)

        # --- Save the final frame of Figure 2 (Timeline series) as a PNG ---
        base_name, _ = os.path.splitext(output_filename)
        png_filename = f"{base_name}_timeline.png"

        # Save Figure 2 directly without altering or repositioning the tracking marker
        print(f"Saving final timeline plot to: {png_filename} ... ", end="", flush=True)
        self.fig2.savefig(png_filename, dpi=150, bbox_inches="tight")
        print("done.")

    def on_slider_move(self, val):
        """Fires when the manual scrubbing slider changes state."""
        idx = int(round(val))
        if idx != self.current_idx:
            self.current_idx = idx
            self.update_plot(self.current_idx)

    def advance_frame_by_timer(self):
        """Timer callback loop that increments index."""
        next_idx = (self.current_idx + 1) % self.num_frames
        self.slider.set_val(next_idx)

    def on_play_click(self, event):
        """Action performed when clicking Play/Pause."""
        if self.playing:
            self.playing = False
            self.timer.stop()
            self.btn_play.label.set_text("▶ Play")
        else:
            self.playing = True
            self.timer.start()
            self.btn_play.label.set_text("⏸ Pause")
        self.fig.canvas.draw_idle()

    def on_prev_click(self, event):
        """Jumps frame back. Halts auto-play."""
        self.halt_playback()
        prev_idx = (self.current_idx - 1) % self.num_frames
        self.slider.set_val(prev_idx)

    def on_next_click(self, event):
        """Jumps frame forward. Halts auto-play."""
        self.halt_playback()
        next_idx = (self.current_idx + 1) % self.num_frames
        self.slider.set_val(next_idx)

    def on_speed_click(self, event):
        """Cycles the frame-rate timer through available increments."""
        self.speed_idx = (self.speed_idx + 1) % len(self.speeds)
        self.timer.interval = self.speeds[self.speed_idx]

        labels = ["Fast", "Med", "Slow"]
        self.btn_speed.label.set_text(f"Speed: {labels[self.speed_idx]}")
        self.fig.canvas.draw_idle()

    def halt_playback(self):
        """Gracefully halts ongoing playback state."""
        if self.playing:
            self.playing = False
            self.timer.stop()
            self.btn_play.label.set_text("▶ Play")
            self.fig.canvas.draw_idle()

    def show(self):
        plt.show()


# --- CLI Parser Setup ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CM1 Vertical Velocity (w) Spectra Interactive Animator."
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="List of NetCDF output files to animate (e.g., cm1out_000001.nc cm1out_000002.nc ...)",
    )
    parser.add_argument(
        "--var",
        default="winterp",
        help="Variable name in NetCDF file (default: winterp)",
    )
    parser.add_argument(
        "--pbl-bot",
        type=float,
        default=0.0,
        help="Bottom limit to integrate heights in km (default: 0.0)",
    )
    parser.add_argument(
        "--pbl-top",
        type=float,
        default=0.84,
        help="Top limit to integrate heights in km (default: 0.84)",
    )
    parser.add_argument(
        "--nsmooth",
        type=int,
        default=5,
        help="Running-mean smooth spectral width points (default: 5)",
    )
    parser.add_argument(
        "--no-detrend",
        action="store_true",
        help="Do not subtract the horizontal mean before performing FFT",
    )
    parser.add_argument(
        "--no-window",
        action="store_true",
        help="Do not apply 2D Hanning window to inputs",
    )
    parser.add_argument(
        "--save-video",
        type=str,
        default=None,
        help="Save animation directly to specified path (ends in .mp4 or .gif) and exit",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=5,
        help="Frames per second for saved output (default: 5)",
    )

    args = parser.parse_args()

    found_files = args.files
    sorted_files = sorted(found_files, key=extract_sequence_number)

    for f in sorted_files:
        if not os.path.exists(f):
            print(f"Error: File not found: '{f}'")
            sys.exit(1)

    print(f"Found and verified {len(sorted_files)} NetCDF sequence files.")

    # Headless backend execution check to prevent X11 display errors on Derecho / remote nodes
    if args.save_video is not None:
        matplotlib.use("Agg")

    # Guard Check for headless environments if user wants interactive GUI
    if args.save_video is None:
        try:
            plt.figure()
            plt.close()
        except Exception:
            print("\n" + "=" * 80)
            print(
                "CRITICAL DISPLAY ERROR: Matplotlib was unable to open a graphical window."
            )
            print(
                "To save direct files headlessly, specify a valid path with the save argument:"
            )
            print(
                "  python cm1_w_spectra_animated.py cm1out_*.nc --save-video output.gif"
            )
            print(
                "  python cm1_w_spectra_animated.py cm1out_*.nc --save-video output.mp4"
            )
            print("=" * 80 + "\n")
            sys.exit(1)

    # Launch application wrapper
    animator = CM1SpectraAnimator(
        files=sorted_files,
        var=args.var,
        pbl_bot_km=args.pbl_bot,
        pbl_top_km=args.pbl_top,
        nsmooth=args.nsmooth,
        detrend=not args.no_detrend,
        window=not args.no_window,
    )

    if args.save_video is not None:
        # Build clean layout without slider controls for presentations and save
        animator.build_gui(skip_widgets=True)
        animator.save_animation(args.save_video, fps=args.fps)
    else:
        # Standard interactive workspace
        animator.build_gui(skip_widgets=False)
        animator.show()
