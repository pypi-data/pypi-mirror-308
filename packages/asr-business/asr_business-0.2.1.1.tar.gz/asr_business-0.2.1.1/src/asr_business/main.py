import logging
import os
from logging.handlers import TimedRotatingFileHandler

from .asr import Asr
from .vad import Vad

logger = logging.getLogger("server.vad_info.log")


def setup_logger(log_dir):
    """
    配置日志
    :param log_dir: 日志文件目录
    :return: logger实例
    """
    os.makedirs(log_dir, exist_ok=True)

    logger.propagate = False
    logger.setLevel(logging.INFO)

    # 避免重复添加handler
    if not logger.handlers:
        log_file = os.path.join(log_dir, "vad_info.log")
        # when='H' 表示每小时轮转
        # interval=1 表示间隔为1小时
        # encoding='utf-8' 设置编码
        handler = TimedRotatingFileHandler(
            log_file,
            when='H',  # 按小时切分
            interval=1,  # 每1小时切分一次
            backupCount=168,  # 保留最近168个文件（7天）
            encoding='utf-8'
        )

        # 设置后缀格式为 .YYYY-MM-DD_HH
        handler.suffix = "%Y-%m-%d_%H"

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


class Inke_asr:
    def __init__(self,
                 asr_model_path="",
                 punc_model_path="",
                 vad_model_path="",
                 batch_size=40,
                 num_process=1,
                 log_dir="",
                 device="cuda:0"):
        """
        :param asr_model_path: asr模型路径
        :param punc_model_path: 标点生成模型路径
        :param vad_model_path: 静音检测模型路径
        :param batch_size: 批处理大小
        :param num_process: 进程数
        :param device: 设备id
        """
        self.logger = setup_logger(log_dir)
        self.asr = Asr(asr_model_path=asr_model_path, punc_model_path=punc_model_path, batch_size=batch_size,
                       device=device)
        self.vad = Vad(vad_model_path=vad_model_path, num_process=num_process, batch_size=batch_size)

    def transcribe(self, audios):
        # 进行静音检测
        valid_audios, vad_result = self.vad.silence_detection(audios)
        # 添加vad静音检测日志
        if vad_result:
            self.logger.info("vad result is: {}".format(vad_result))
        # 进行asr识别，如果文件列表不为空，进行asr翻译
        if valid_audios:
            asr_result = self.asr.transcribe(valid_audios)
            asr_result.extend(vad_result)
            return asr_result
        else:
            return vad_result
