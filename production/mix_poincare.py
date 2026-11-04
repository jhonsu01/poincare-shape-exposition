"""Une las escenas de Poincare con narracion, fondo sonoro y efectos propios. Uso: mix_poincare.py <en|es> <version>"""
import json
import subprocess
import sys
from pathlib import Path

BASE = Path("D:/Dev/mathdb-video/poincare")
AUDIO = Path("D:/Dev/docker-phonon/projects/poincare/out")
SFX = Path("D:/Dev/mathdb-video/sfx")


def run(*args):
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *args], check=True)


def main():
    lang, version = sys.argv[1], sys.argv[2]
    work = BASE / lang
    timeline = json.loads((work / "timeline.json").read_text(encoding="utf-8"))
    total = timeline[-1]["start"] + timeline[-1]["duration"]

    video_list = work / "anim_list.txt"
    video_list.write_text("".join(f"file 'anim/scene_{s['n']:02d}.mp4'\n" for s in timeline), encoding="utf-8")
    run("-f", "concat", "-safe", "0", "-i", str(video_list), "-c", "copy", str(work / "video_only.mp4"))

    voices = []
    for s in timeline:
        voices += ["-i", str(AUDIO / lang / f"scene_{s['n']:02d}.wav")]
    parts = "".join(f"[{i}:a]aresample=48000,apad=whole_dur={s['duration']}[v{i}];" for i, s in enumerate(timeline))
    joined = "".join(f"[v{i}]" for i in range(len(timeline)))
    run(*voices, "-filter_complex", f"{parts}{joined}concat=n={len(timeline)}:v=0:a=1[o]", "-map", "[o]", str(work / "narration.wav"))

    expr = "0.5*sin(2*PI*65.41*t)*(0.7+0.3*sin(2*PI*t/13))+0.3*sin(2*PI*98*t)*(0.7+0.3*sin(2*PI*t/19))+0.2*sin(2*PI*130.81*t)*(0.7+0.3*sin(2*PI*t/29))"
    run("-f", "lavfi", "-i", f"aevalsrc={expr}:s=48000:d={total}", "-f", "lavfi", "-i", f"anoisesrc=color=brown:r=48000:a=0.4:d={total}",
        "-filter_complex", f"[1:a]lowpass=f=300[n];[0:a][n]amix=inputs=2:weights='1 0.5':normalize=0,afade=t=in:d=4,afade=t=out:st={total - 5}:d=5,volume=0.045[o]",
        "-map", "[o]", str(work / "bed.wav"))

    starts = {s["n"]: s["start"] for s in timeline}
    durations = {s["n"]: s["duration"] for s in timeline}
    cues = [("whoosh.wav", starts[n] - 0.4, 0.09) for n in range(2, 11)]
    cues.append(("riser.wav", starts[6] + durations[6] * 0.62 - 4.0, 0.09))
    cues.append(("ding.wav", starts[6] + durations[6] * 0.62, 0.08))
    cues.append(("ding.wav", starts[8] + durations[8] * 0.85, 0.08))

    inputs = ["-i", str(work / "narration.wav"), "-i", str(work / "bed.wav")]
    filters = []
    labels = "[1:a][2:a]"
    for i, (name, at, gain) in enumerate(cues):
        inputs += ["-i", str(SFX / name)]
        delay = int(max(at, 0) * 1000)
        filters.append(f"[{i + 3}:a]aresample=48000,aformat=channel_layouts=mono,volume={gain},adelay={delay}:all=1[s{i}]")
        labels += f"[s{i}]"
    graph = ";".join(filters) + f";{labels}amix=inputs={len(cues) + 2}:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11[o]"
    final = work / f"poincare_{lang}_{version}.mp4"
    run("-i", str(work / "video_only.mp4"), *inputs, "-filter_complex", graph, "-map", "0:v", "-map", "[o]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(final))
    print(final)


if __name__ == "__main__":
    main()
