from  subprocess import Popen, PIPE, DEVNULL


class VideoGeneratorImage:
    
    def __init__(self, output_file, temp_path):
        self._frame_index = 0
        self._temp_dir = temp_path
        self._output_file = output_file

    
    def append_image(self, image):
        img_path = f"{self._temp_dir}/frame_{self._frame_index:05}.bmp"
        image.save(img_path, format="bmp")
        self._frame_index += 1

          
    def close(self, fps=60):

        command = ["ffmpeg",
                '-framerate', f'{fps}',
                '-i', f"{self._temp_dir}/frame_%05d.bmp",
                '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', #pad odd dimension images
                '-r', f'{fps}',
                '-crf', '1', # quality - lower # is higher quality
                '-pix_fmt', 'yuv420p',
                '-y',    # overwrite
                self._output_file ]

        print("CMD:", " ".join(command))
        self._proc = Popen(command, text=False)
        self._proc.wait()
        print("done")


class VideoGenerator:
    
    def __init__(self, output_file, fps=60, live_preview=False, subsample=1, subsample_multiplier=1):
       
        command = ["ffmpeg",
            '-framerate', f'{fps}',
            '-f', 'image2pipe', # input from pipe
            '-vcodec', 'bmp', # input codec
            '-i', '-', # data from stdin
            '-pix_fmt', 'yuv420p',
            '-crf', '1', # quality - lower # is higher quality
            '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', #pad odd dimension images
            '-y',    # overwrite
            output_file ]
        self._proc = Popen(command, stdin=PIPE, stdout=DEVNULL, text=False)

        if live_preview:
            preview_cmd = ["ffplay",
                '-f', 'image2pipe', # input from pipe
                '-vcodec', 'bmp', # input codec
                '-i', '-', # data from stdin
                '-crf', '1', # quality - lower # is higher quality
                '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2', #pad odd dimension images
                ]
            self._preview_proc = Popen(preview_cmd, stdin=PIPE, stdout=DEVNULL, text=False)
        else:
            self._preview_proc = None
             
        self._subsample = subsample
        self._subsample_multiplier = subsample_multiplier
        self._frame_index = 0


    def append_image(self, image, force=False):

        save_image = False
        if self._frame_index % int(self._subsample) == 0:
            save_image = True
            self._subsample *= self._subsample_multiplier

        if save_image or force:
            image.save(self._proc.stdin, format="bmp")
            self._proc.stdin.flush()
            if self._preview_proc:
                image.save(self._preview_proc.stdin, format="bmp")
                self._preview_proc.stdin.flush()
            
        self._frame_index += 1
       
         
    def close(self):
        print("closing video...")
        try:
            self._proc.stdin.close()
            self._proc.wait()
        except Exception as e:
            print("failed to close ffmpeg process", e)

        if self._preview_proc:
            print("closing preview...")
            try:
                self._preview_proc.kill()
            except Exception as e:
                print("failed to close ffplay process", e)

    #adding enter and exit turn VideoGenerator into a context manager allowing it to be used in a with statement to autoclose
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


            
        