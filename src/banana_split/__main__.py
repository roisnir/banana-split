import os
import subprocess
import csv
import sys
from tqdm import tqdm


def split_video(video_name, start_dur=None, end_dur=None, output_name=None):
    args = ['ffmpeg', '-i', video_name]
    if start_dur:
        args += ('-ss', start_dur)
    if end_dur:
        args += ('-to', end_dur)
    args += ('-c', 'copy', output_name)
    p = subprocess.Popen(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    err, out = p.communicate()
    if p.returncode != 0:
        raise ValueError(f'ffmpeg resulted with return code {p.returncode}\r\nstderr:\r\n{err}\r\nstdout:\r\n{out}')
    return output_name

def split_videos_batch(input_csv_path, videos_dir='.', output_dir='.'):
    """
    input csv format:
    file,start,end,name
    'in'

    """
    videos = list(csv.DictReader(open(input_csv_path, 'r')))
    for vid in tqdm(videos):
        vid_name, _, vid_ext = vid['file'].rpartition('.')
        output_path = os.path.join(output_dir, f"{vid_name}_{vid['name']}.{vid_ext}")
        input_path = os.path.join(videos_dir, vid['file'])
        split_video(input_path, vid['start'], vid['end'], output_path)
    print(f'trimmed {len(videos)} videos. saved at {output_dir}')

def main():
    split_videos_batch(*sys.argv[1:])

if __name__ == '__main__':
    main()
