import wavelink
from dataclasses import dataclass
from typing import Any

@dataclass
class InfoTrack:
    title: str
    album: str
    artist: str
    artwork: str
    author: str

class InfoTrack_Class(wavelink.Playable):
    """
    คลาสสำหรับจัดการข้อมูลแทร็กเพลงที่ได้รับจาก Playable\n
    ซึ่งจะเก็บข้อมูลต่างๆ ที่เกี่ยวข้องกับแทร็กเพลง\n
    เช่น ชื่อแทร็ก, อัลบั้ม, ศิลปิน, ภาพปก และข้อมูลดิบ
    """

    def __init__(self, title: str, album: str, artwork: str, author: str, data: Any):
        """
        กำหนดค่าเริ่มต้นสำหรับข้อมูลแทร็กเพลง

        Args:
            title (str): ชื่อของแทร็กเพลง
            album (str): ชื่ออัลบั้มของแทร็ก
            artwork (str): URL ของภาพหน้าปก
            author (str): ชื่อผู้แต่งหรือศิลปิน
            data (Any): ข้อมูลดิบที่มาจาก Wavelink
        """
        super().__init__(data)
        self._title = title
        self._album = album
        self._artwork = artwork
        self._author = author
        self.data = data
        self._info = None

    @property
    def title(self):
        """
        รับค่าชื่อของแทร็ก

        คืนค่าชื่อแทร็กจากตัวแปร _title ซึ่งถูกกำหนดใน constructor

        Returns:
            str: ชื่อของแทร็ก
        """
        return self._title

    @title.setter
    def title(self, value: str):
        """
        ตั้งค่าชื่อของแทร็ก

        กำหนดค่าชื่อแทร็กใหม่ให้กับตัวแปร _title

        Args:
            value (str): ชื่อของแทร็กที่ต้องการตั้งค่าใหม่
        """
        self._title = value

    @property
    def album(self):
        """
        รับค่าอัลบัมของแทร็ก

        คืนค่าชื่ออัลบัมจากตัวแปร _album ซึ่งถูกกำหนดใน constructor

        Returns:
            str: ชื่อของอัลบัม
        """
        return self._album

    @album.setter
    def album(self, value: str):
        """
        ตั้งค่าอัลบัมของแทร็ก

        กำหนดค่าอัลบัมใหม่ให้กับตัวแปร _album

        Args:
            value (str): ชื่อของอัลบัมที่ต้องการตั้งค่าใหม่
        """
        self._album = value

    @property
    def artwork(self):
        """
        รับค่า artwork ของแทร็ก

        คืนค่าภาพปกอัลบัมหรือ artwork ของแทร็กจากตัวแปร _artwork

        Returns:
            str: ลิงก์ไปยังภาพ artwork ของแทร็ก
        """
        return self._artwork

    @artwork.setter
    def artwork(self, value: str):
        """
        ตั้งค่า artwork ของแทร็ก

        กำหนดค่า artwork ใหม่ให้กับตัวแปร _artwork

        Args:
            value (str): ลิงก์ของ artwork ที่ต้องการตั้งค่าใหม่
        """
        self._artwork = value

    @property
    def author(self):
        """
        รับค่าผู้แต่ง (author) ของแทร็ก

        คืนค่าชื่อผู้แต่งจากตัวแปร _author ซึ่งถูกกำหนดใน constructor

        Returns:
            str: ชื่อผู้แต่งของแทร็ก
        """
        return self._author

    @author.setter
    def author(self, value: str):
        """
        ตั้งค่าผู้แต่ง (author) ของแทร็ก

        กำหนดชื่อผู้แต่งใหม่ให้กับตัวแปร _author

        Args:
            value (str): ชื่อของผู้แต่งที่ต้องการตั้งค่าใหม่
        """
        self._author = value

    @property
    def info(self) -> InfoTrack:
        """
        คืนค่าข้อมูลทั้งหมดของแทร็กในรูปแบบ InfoTrack

        ถ้าข้อมูล info ยังไม่ถูกตั้งค่า จะทำการสร้าง InfoTrack ใหม่และเก็บไว้ใน _info
        ข้อมูลที่คืนมาจะรวมถึงชื่อแทร็ก, อัลบัม, ผู้แต่ง, artwork และข้อมูลอื่นๆ ที่เกี่ยวข้อง

        Returns:
            InfoTrack: ข้อมูลของแทร็กในรูปแบบ InfoTrack

        Note:
            ถ้าไม่มีการตั้งค่าข้อมูลของแทร็ก อาจทำให้เกิดข้อผิดพลาด
        """
        if not self._info:
            self._info = InfoTrack(
                title=self._title,
                album=self._album,
                artist=self._author,  # ใช้ author หรือ artist ขึ้นอยู่กับความต้องการ
                artwork=self._artwork,
                author=self._author
            )
        return self._info