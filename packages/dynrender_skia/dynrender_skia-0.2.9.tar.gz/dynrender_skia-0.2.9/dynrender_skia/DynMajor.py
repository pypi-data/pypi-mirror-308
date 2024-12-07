"""
@File    :   DynMajor.py
@Time    :   2023/11/13 19:15:46
@Author  :   Polyisoprene
@Version :   1.0
@Desc    :   None
"""

from abc import ABC, abstractmethod
from math import ceil
from os import path
from typing import Optional

import emoji
import numpy as np
import skia
from dynamicadaptor.Content import RichTextDetail
from dynamicadaptor.Content import Text
from dynamicadaptor.Majors import Major, RichTextNodes
from loguru import logger

from .DynStyle import PolyStyle
from .DynText import BiliText
from .DynTools import paste, get_pictures, merge_pictures


class AbstractMajor(ABC):
    def __init__(self, src_path: str, style: PolyStyle, dyn_major: Major = None) -> None:
        self.style = style
        self.major = dyn_major
        self.text_font = skia.Font(
            skia.Typeface.MakeFromName(self.style.font.font_family, self.style.font.font_style),
            self.style.font.font_size.text,
        )
        self.emoji_font = skia.Font(
            skia.Typeface.MakeFromName(self.style.font.emoji_font_family, self.style.font.font_style),
            self.style.font.font_size.text,
        )
        self.src_path = src_path
        self.canvas = None

    @abstractmethod
    async def run(self, repost) -> Optional[np.ndarray]:
        pass

    async def draw_text(
        self,
        canvas,
        text: str,
        font_size,
        pos: tuple,
        font_color: tuple,
        font_style=None,
    ):
        paint = skia.Paint(AntiAlias=True, Color=skia.Color(*font_color))
        if font_style is not None:
            self.text_font = skia.Font(
                skia.Typeface.MakeFromName(self.style.font.font_family, font_style),
                self.style.font.font_size.text,
            )
        self.text_font.setSize(font_size)  # todo:repitition in DynMajor.py line 88
        self.emoji_font.setSize(font_size)
        text = text.replace("\t", "")
        emoji_info = await self.get_emoji_text(text)
        total = len(text) - 1
        x, y, x_bound, y_bound, y_int = pos
        offset = 0
        while offset <= total:
            j = text[offset]
            if j == "\n":
                break
            if offset in emoji_info.keys():
                j = emoji_info[offset][1]
                offset = emoji_info[offset][0]
                font = self.emoji_font
            else:
                offset += 1
                font = self.text_font
            if font.textToGlyphs(j)[0] == 0:
                if typeface := skia.FontMgr().matchFamilyStyleCharacter(
                    self.style.font.font_family,
                    self.style.font.font_style,
                    ["zh", "en"],
                    ord(j[0]),
                ):
                    font = skia.Font(typeface, font_size)
                else:
                    font = self.text_font
            measure = font.measureText(j)
            blob = skia.TextBlob(j, font)
            canvas.drawTextBlob(blob, x, y, paint)
            x += measure
            if x > x_bound:
                y += y_int
                if y >= y_bound:
                    blob = skia.TextBlob("...", font)
                    canvas.drawTextBlob(blob, x, y - y_int, paint)
                    break
                x = pos[0]

    async def get_emoji_text(self, text):
        result = emoji.emoji_list(text)
        temp = {}
        for i in result:
            temp[i["match_start"]] = [i["match_end"], i["emoji"]]
        return temp

    async def draw_shadow(self, canvas, pos: tuple, corner: int, bg_color):
        x, y, width, height = pos
        rec = skia.Rect.MakeXYWH(x, y, width, height)
        paint = skia.Paint(
            Color=skia.Color(*bg_color),
            AntiAlias=True,
            ImageFilter=skia.ImageFilters.DropShadow(0, 0, 10, 10, skia.Color(120, 120, 120)),
        )
        if corner != 0:
            canvas.drawRoundRect(rec, corner, corner, paint)
        else:
            canvas.drawRect(rec, paint)

    async def make_round_cornor(self, img, corner: int):
        surface = skia.Surface(img.width(), img.height())
        mask = surface.getCanvas()
        paint = skia.Paint(
            Style=skia.Paint.kFill_Style,
            Color=skia.Color(255, 255, 255, 255),
            AntiAlias=True,
        )
        rect = skia.Rect.MakeXYWH(0, 0, img.width(), img.height())
        mask.drawRoundRect(rect, corner, corner, paint)
        image_array = np.bitwise_and(
            img.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType),
            mask.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType),
        )
        return skia.Image.fromarray(image_array, colorType=skia.ColorType.kRGBA_8888_ColorType)

    async def make_tag(self, tag: str, font_size: int):
        text_font = self.text_font
        if text_font.textToGlyphs(text=tag[0])[0] == 0:  # type: ignore
            if typeface := skia.FontMgr().matchFamilyStyleCharacter(
                self.style.font.font_family,
                self.style.font.font_style,
                ["zh", "en"],
                ord(tag[0]),
            ):
                text_font = skia.Font(typeface, self.style.font.font_size.text)
        text_font.setSize(font_size)
        size = text_font.measureText(text=tag)  # type: ignore
        surface = skia.Surface(int(size + 20), int(text_font.getSize() + 20))
        canvas = surface.getCanvas()
        canvas.clear(skia.Color(*self.style.color.font_color.name_big_vip))
        blob = skia.TextBlob(text=tag, font=text_font)  # type: ignore
        paint = skia.Paint(AntiAlias=True, Color=skia.Color4f.kWhite)
        canvas.drawTextBlob(blob, 10, int(text_font.getSize() + 5), paint)
        tag_img = skia.Image.fromarray(
            array=canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType),
            colorType=skia.ColorType.kRGBA_8888_ColorType,
        )  # type: ignore
        tag_img = await self.make_round_cornor(tag_img, 10)
        await paste(self.canvas, tag_img, (1010 - tag_img.width(), 50))

    async def make_sub_tag(self, sub_tag: str, font_size: int):
        text_font = self.text_font
        if text_font.textToGlyphs(text=sub_tag[0])[0] == 0:  # type: ignore
            if typeface := skia.FontMgr().matchFamilyStyleCharacter(
                self.style.font.font_family,
                self.style.font.font_style,
                ["zh", "en"],
                ord(sub_tag[0]),
            ):
                text_font = skia.Font(typeface, self.style.font.font_size.text)
        text_font.setSize(font_size)
        size = text_font.measureText(text=sub_tag)  # type: ignore
        surface = skia.Surface(int(size + 20), int(text_font.getSize() + 20))
        canvas = surface.getCanvas()
        canvas.clear(skia.Color(0, 0, 0, 150))
        blob = skia.TextBlob(text=sub_tag, font=text_font)  # type: ignore
        paint = skia.Paint(AntiAlias=True, Color=skia.Color4f.kWhite)
        canvas.drawTextBlob(blob, 10, int(text_font.getSize() + 5), paint)
        sub_title_img = skia.Image.fromarray(
            array=canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType),
            colorType=skia.ColorType.kRGBA_8888_ColorType,
        )  # type: ignore
        await paste(self.canvas, await self.make_round_cornor(sub_title_img, 10), (80, 525))


class BiliMajor:
    def __init__(self, static_path: str, style: PolyStyle) -> None:
        self.src_path = path.join(static_path, "Src")
        self.style = style

    async def run(self, dyn_major: Major, repost: bool = False) -> Optional[np.ndarray]:
        try:
            major_type = dyn_major.type
            if major_type == "MAJOR_TYPE_DRAW":
                return await DynMajorDraw(self.style, items=dyn_major.draw.items).run(repost)
            elif major_type == "MAJOR_TYPE_ARCHIVE":
                return await DynMajorArchive(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_LIVE_RCMD":
                return await DynMajorLiveRcmd(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_OPUS":
                return await DynMajorOpus(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_ARTICLE":
                return await DynMajorArticle(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_COMMON":
                return await DynMajorCommon(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_MUSIC":
                return await DynMajorMusic(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_PGC":
                return await DynMajorPgc(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_MEDIALIST":
                return await DynMajorMediaList(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_COURSES":
                return await DynMajorCourses(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_UGC_SEASON":
                return await DynMajorUgc(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_LIVE":
                return await DynMajorLive(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_NONE":
                return await DynMajorNone(self.src_path, self.style, dyn_major).run(repost)
            elif major_type == "MAJOR_TYPE_BLOCKED":
                return await DynMajorBlocked(self.src_path, self.style, dyn_major).run(repost)
            else:
                logger.warning(f"{major_type} is not supported")
                return None
        except Exception as e:
            logger.exception(e)
            return None


class DynMajorDraw:
    """Dynamic picture drawing class"""

    def __init__(self, style: PolyStyle, items=None) -> None:
        self.style = style
        self.items = items

    async def run(self, repost: bool) -> Optional[np.ndarray]:
        """
        make image of major draw
        @param repost: bool
        @return:
        """
        try:
            item_count = len(self.items)
            background_color = self.style.color.background.repost if repost else self.style.color.background.normal
            if item_count == 1:
                return await self.single_img(background_color, self.items)
            elif item_count in {2, 4}:
                return await self.dual_img(background_color, self.items)
            else:
                return await self.triplex_img(background_color, self.items)
        except Exception:
            logger.exception("Error")
            return None

    async def single_img(self, background_color: tuple, items) -> np.ndarray:
        src = items[0].src or items[0].url
        img_height = items[0].height
        img_width = items[0].width
        if img_height / img_width > 4:
            img_url = f"{src}@{600}w_{800}h_!header.webp"
        else:
            img_url = src
        img: skia.Image = await get_pictures(img_url)
        if img is not None:
            img = img.resize(width=1008, height=int(img.height() * 1008 / img.width()))
            surface = skia.Surface(1080, img.height() + 20)
            canvas = surface.getCanvas()
            canvas.clear(skia.Color(*background_color))
            await paste(canvas, img, (36, 10), clear_background=True)
        else:
            logger.warning("Image is None, render placeholder")
            surface = skia.Surface(1080, 1080)
            canvas = surface.getCanvas()
            canvas.clear(skia.Color(*background_color))

        return canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)

    async def dual_img(self, background_color: tuple, items):
        url_list = []
        for item in items:
            src = item.src or item.url
            img_height = item.height
            img_width = item.width
            if img_height / img_width > 3:
                url_list.append(f"{src}@520w_520h_!header.webp")
            else:
                url_list.append(f"{src}@520w_520h_1e_1c.webp")
        imgs = await get_pictures(url_list, (520, 520))
        num = len(url_list) / 2
        back_size = int(num * 520 + 20 * num)
        surface = skia.Surface(1080, back_size)
        canvas = surface.getCanvas()
        canvas.clear(skia.Color(*background_color))

        x, y = 15, 10
        for i in imgs:
            if i is not None:
                await paste(canvas, i, (x, y), clear_background=True)
            x += 530
            if x > 1000:
                x = 15
                y += 530
        return canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)

    async def triplex_img(self, background_color: tuple, items):
        url_list = []
        for item in items:
            src = item.src or item.url
            img_height = item.height
            img_width = item.width
            if img_height / img_width > 3:
                url_list.append(f"{src}@260w_260h_!header.webp")
            else:
                url_list.append(f"{src}@260w_260h_1e_1c.webp")
        num = ceil(len(items) / 3)

        imgs = await get_pictures(url_list, (346, 346))

        back_size = int(num * 346 + 20 * num)
        surface = skia.Surface(1080, back_size)
        canvas = surface.getCanvas()
        canvas.clear(skia.Color(*background_color))
        x, y = 11, 10
        for img in imgs:
            if img is not None:
                await paste(canvas, img, (x, y), clear_background=True)
            x += 356
            if x > 1000:
                x = 11
                y += 356
        return canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


class DynMajorArchive(AbstractMajor):
    async def run(self, repost):
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 695)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        tv = skia.Image.open(path.join(self.src_path, "tv.png")).resize(130, 130)
        try:
            cover = await get_pictures(f"{self.major.archive.cover}@505w_285h_1c.webp", (1010, 570))

            await self.draw_shadow(self.canvas, (35, 25, 1010, 655), 20, background_color)
            rec = skia.Rect.MakeXYWH(35, 25, 1010, 665)
            self.canvas.clipRRect(skia.RRect(rec, 20, 20), skia.ClipOp.kIntersect)
            await self.draw_text(
                self.canvas,
                self.major.archive.title,
                self.style.font.font_size.text,
                (60, 650, 980, 600, 10),
                self.style.color.font_color.text,
            )
            await paste(self.canvas, cover, (35, 25))
            await paste(self.canvas, tv, (905, 455))
            if self.major.archive.badge is not None and self.major.archive.badge.text != "":
                await self.make_tag(self.major.archive.badge.text, self.style.font.font_size.text)
            await self.make_sub_tag(self.major.archive.duration_text, self.style.font.font_size.title)
            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception:
            logger.exception("Error")
            return None


class DynMajorLiveRcmd(AbstractMajor):
    async def run(self, repost) -> Optional[np.ndarray]:
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 695)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        try:
            cover = await get_pictures(
                f"{self.major.live_rcmd.content.live_play_info.cover}@505w_285h_1c.webp",
                (1010, 570),
            )

            await self.draw_shadow(self.canvas, (35, 25, 1010, 655), 20, background_color)
            rec = skia.Rect.MakeXYWH(35, 25, 1010, 665)
            self.canvas.clipRRect(skia.RRect(rec, 20, 20), skia.ClipOp.kIntersect)

            await self.draw_text(
                self.canvas,
                self.major.live_rcmd.content.live_play_info.title,
                self.style.font.font_size.text,
                (60, 650, 980, 600, 10),
                self.style.color.font_color.text,
            )
            await paste(self.canvas, cover, (35, 25))
            await self.make_tag("直播中", self.style.font.font_size.text)
            await self.make_sub_tag(
                self.major.live_rcmd.content.live_play_info.watched_show.text_large,
                self.style.font.font_size.title,
            )
            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception:
            logger.exception("Error")
            return None


class DynMajorOpus(AbstractMajor):
    @staticmethod
    def _convert_to_rich_text_detail(rich_text_node: RichTextNodes) -> RichTextDetail:
        """
        Magic method to convert rich_text_node to RichTextDetail.
        Simplifies the process by directly integrating condition into assignment.
        :param rich_text_node: RichTextNodes
        :return: RichTextDetail
        """
        return RichTextDetail(
            type=rich_text_node.type,
            text=rich_text_node.text,
            orig_text=rich_text_node.orig_text,
            emoji=rich_text_node.emoji.dict() if rich_text_node.type == "RICH_TEXT_NODE_TYPE_EMOJI" else None,
        )

    async def run(self, repost) -> Optional[np.ndarray]:
        pics = []
        try:
            if self.major.opus.title:
                title = await self.make_title(self.major.opus.title, repost)
                pics.append(title)
        except Exception as e:
            logger.exception(e)
        try:
            if self.major.opus.summary:
                # self.style.font.font_style=skia.FontStyle().Normal()
                dyn_text = Text(
                    text=self.major.opus.summary.text,
                    topic=None,
                    rich_text_nodes=[
                        self._convert_to_rich_text_detail(node) for node in self.major.opus.summary.rich_text_nodes
                    ],
                )
                text_img = await BiliText(path.dirname(self.src_path), self.style).run(dyn_text, repost)
                pics.append(text_img)
        except Exception as e:
            logger.exception(e)
        try:
            if self.major.opus.pics:
                cover = await DynMajorDraw(self.style, items=self.major.opus.pics).run(repost)
                pics.append(cover)
        except Exception as e:
            logger.exception(e)
        if not pics:
            return None
        return await merge_pictures(pics)

    async def make_title(self, title, repost):
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, self.style.font.font_size.name + 20)
        canvas = surface.getCanvas()
        canvas.clear(skia.Color(*background_color))
        await self.draw_text(
            canvas,
            title,
            self.style.font.font_size.name,
            (45, int((self.style.font.font_size.name + 40) / 2), 1035, 40, 0),
            self.style.color.font_color.text,
            font_style=skia.FontStyle().Bold(),
        )
        return canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)


class DynMajorArticle(AbstractMajor):
    async def run(self, repost) -> Optional[np.ndarray]:
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 640)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        try:
            await self.draw_shadow(self.canvas, (35, 20, 1010, 600), 20, background_color)

            rec = skia.Rect.MakeXYWH(35, 20, 1010, 600)
            self.canvas.clipRRect(skia.RRect(rec, 20, 20), skia.ClipOp.kIntersect)
            await self.draw_title_and_desc()
            await self.make_cover()
            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception as e:
            logger.exception(e)
            return None

    async def make_cover(self):
        if len(self.major.article.covers) > 1:
            url_list = [f"{i}@360w_360h_1c" for i in self.major.article.covers]
            imgs = await get_pictures(url_list, (330, 330))
            for i, j in enumerate(imgs):
                await paste(self.canvas, j, (35 + i * 340, 20))
        else:
            img = await get_pictures(f"{self.major.article.covers[0]}@647w_150h_1c.webp", (1010, 300))
            await paste(self.canvas, img, (35, 20))

    async def draw_title_and_desc(self):
        title = self.major.article.title
        if len(self.major.article.covers) > 1:
            await self.draw_text(
                self.canvas,
                title,
                self.style.font.font_size.text,
                (50, 410, 960, 330, 0),
                self.style.color.font_color.text,
            )
        else:
            await self.draw_text(
                self.canvas,
                title,
                self.style.font.font_size.text,
                (50, 390, 960, 330, 0),
                self.style.color.font_color.text,
            )
        desc = self.major.article.desc
        await self.draw_text(
            self.canvas,
            desc,
            self.style.font.font_size.title,
            (65, 460, 980, 620, int(self.style.font.font_size.title * 1.8)),
            self.style.color.font_color.sub_title,
        )


class DynMajorCommon(AbstractMajor):
    async def run(self, repost) -> Optional[np.ndarray]:
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 285)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        try:
            await self.draw_shadow(self.canvas, (35, 20, 1010, 245), 20, background_color)
            rec = skia.Rect.MakeXYWH(35, 20, 1010, 245)
            self.canvas.clipRRect(skia.RRect(rec, 20, 20), skia.ClipOp.kIntersect)
            cover = await get_pictures(f"{self.major.common.cover}@245w_245h_1c.webp", (245, 245))
            await paste(self.canvas, cover, (35, 20))
            await self.make_title()
            await self.make_common_tag()
            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception as e:
            logger.exception(e)
            return None

    async def make_title(self):
        title = self.major.common.title
        await self.draw_text(
            self.canvas,
            title,
            self.style.font.font_size.text,
            (310, 120, 950, 120, 0),
            self.style.color.font_color.text,
        )
        sub_title = self.major.common.desc
        await self.draw_text(
            self.canvas,
            sub_title,
            self.style.font.font_size.title,
            (310, 190, 970, 190, 0),
            self.style.color.font_color.sub_title,
        )

    async def make_common_tag(self):
        if self.major.common.badge is not None and self.major.common.badge.text != "":
            self.text_font.setSize(self.style.font.font_size.sub_title)
            size = self.text_font.measureText(self.major.common.badge.text)
            tag_width = int(size + 20)
            surface = skia.Surface(tag_width, int(self.text_font.getSize() + 20))
            canvas = surface.getCanvas()
            canvas.clear(skia.Color(*self.style.color.font_color.name_big_vip))
            blob = skia.TextBlob(self.major.common.badge.text, self.text_font)
            paint = skia.Paint(AntiAlias=True, Color=skia.Color4f.kWhite)
            canvas.drawTextBlob(blob, 10, int(self.text_font.getSize() + 5), paint)
            tag_img = skia.Image.fromarray(
                canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType),
                colorType=skia.ColorType.kRGBA_8888_ColorType,
            )
            await paste(
                self.canvas,
                await self.make_round_cornor(tag_img, 10),
                (280 - tag_width - 20, 40),
            )


class DynMajorMusic(AbstractMajor):
    async def run(self, repost):
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 285)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        try:
            await self.draw_shadow(self.canvas, (35, 20, 1010, 245), 20, background_color)
            rec = skia.Rect.MakeXYWH(35, 20, 1010, 245)
            self.canvas.clipRRect(skia.RRect(rec, 20, 20), skia.ClipOp.kIntersect)
            cover = await get_pictures(f"{self.major.music.cover}@245w_245h_1c.webp", (245, 245))
            await paste(self.canvas, cover, (35, 20))
            await self.make_title()
            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception as e:
            logger.exception(e)
            return None

    async def make_title(self):
        title = self.major.music.title
        await self.draw_text(
            self.canvas,
            title,
            self.style.font.font_size.text,
            (310, 120, 950, 120, 0),
            self.style.color.font_color.text,
        )
        sub_title = self.major.music.label
        await self.draw_text(
            self.canvas,
            sub_title,
            self.style.font.font_size.title,
            (310, 190, 970, 190, 0),
            self.style.color.font_color.sub_title,
        )


class DynMajorPgc(AbstractMajor):
    async def run(self, repost):
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 695)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        tv = skia.Image.open(path.join(self.src_path, "tv.png")).resize(130, 130)
        try:
            cover = await get_pictures(f"{self.major.pgc.cover}@505w_285h_1c.webp", (1010, 570))
            await self.draw_shadow(self.canvas, (35, 25, 1010, 655), 20, background_color)
            rec = skia.Rect.MakeXYWH(35, 25, 1010, 665)
            self.canvas.clipRRect(skia.RRect(rec, 20, 20), skia.ClipOp.kIntersect)
            await self.draw_text(
                self.canvas,
                self.major.pgc.title,
                self.style.font.font_size.text,
                (60, 650, 980, 600, 10),
                self.style.color.font_color.text,
            )
            await paste(self.canvas, cover, (35, 25))
            await paste(self.canvas, tv, (905, 455))
            if self.major.pgc.badge is not None and self.major.pgc.badge.text != "":
                tag = self.major.pgc.badge.text
            else:
                tag = "投稿视频"
            await self.make_tag(tag, self.style.font.font_size.text)
            await self.make_sub_tag(f"{self.major.pgc.stat.play}播放", self.style.font.font_size.title)
            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception:
            logger.exception("Error")
            return None


class DynMajorMediaList(AbstractMajor):
    async def run(self, repost):
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 695)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        tv = skia.Image.open(path.join(self.src_path, "tv.png")).resize(130, 130)
        try:
            cover = await get_pictures(f"{self.major.medialist.cover}@505w_285h_1c.webp", (1010, 570))
            await self.draw_shadow(self.canvas, (35, 25, 1010, 655), 20, background_color)
            rec = skia.Rect.MakeXYWH(35, 25, 1010, 665)
            self.canvas.clipRRect(skia.RRect(rec, 20, 20), skia.ClipOp.kIntersect)
            await self.draw_text(
                self.canvas,
                self.major.medialist.title,
                self.style.font.font_size.text,
                (60, 650, 980, 600, 10),
                self.style.color.font_color.text,
            )
            await paste(self.canvas, cover, (35, 25))
            if self.major.medialist.badge is not None:
                tag = self.major.medialist.badge.text
            else:
                tag = "投稿视频"
            await self.make_tag(tag, self.style.font.font_size.text)
            await self.make_sub_tag(self.major.medialist.sub_title, self.style.font.font_size.title)
            await paste(self.canvas, tv, (905, 455))
            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception as e:
            logger.exception(e)
            return None


class DynMajorCourses(AbstractMajor):
    async def run(self, repost):
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 695)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        tv = skia.Image.open(path.join(self.src_path, "tv.png")).resize(130, 130)
        try:
            cover = await get_pictures(f"{self.major.courses.cover}@505w_285h_1c.webp", (1010, 570))
            await self.draw_shadow(self.canvas, (35, 25, 1010, 655), 20, background_color)
            rec = skia.Rect.MakeXYWH(35, 25, 1010, 665)
            self.canvas.clipRRect(skia.RRect(rec, 20, 20), skia.ClipOp.kIntersect)
            await self.draw_text(
                self.canvas,
                self.major.courses.title,
                self.style.font.font_size.text,
                (60, 650, 980, 600, 10),
                self.style.color.font_color.text,
            )
            await paste(self.canvas, cover, (35, 25))
            if self.major.courses.badge is not None and self.major.courses.badge.text != "":
                tag = self.major.courses.badge.text
            else:
                tag = "投稿视频"
            await self.make_tag(tag, self.style.font.font_size.text)
            await self.make_sub_tag(self.major.courses.desc, self.style.font.font_size.title)
            await paste(self.canvas, tv, (905, 455))
            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception as e:
            logger.exception(e)
            return None


class DynMajorUgc(AbstractMajor):
    async def run(self, repost):
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 695)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        tv = skia.Image.open(path.join(self.src_path, "tv.png")).resize(130, 130)
        try:
            cover = await get_pictures(f"{self.major.ugc_season.cover}@505w_285h_1c.webp", (1010, 570))
            await self.draw_shadow(self.canvas, (35, 25, 1010, 655), 20, background_color)
            rec = skia.Rect.MakeXYWH(35, 25, 1010, 665)
            self.canvas.clipRRect(skia.RRect(rec, 20, 20), skia.ClipOp.kIntersect)
            await self.draw_text(
                self.canvas,
                self.major.ugc_season.title,
                self.style.font.font_size.text,
                (60, 650, 980, 600, 10),
                self.style.color.font_color.text,
            )
            await paste(self.canvas, cover, (35, 25))
            if self.major.ugc_season.badge is not None and self.major.ugc_season.badge.text != "":
                tag = self.major.ugc_season.badge.text
            else:
                tag = "投稿视频"
            await self.make_tag(tag, self.style.font.font_size.text)
            await self.make_sub_tag(self.major.ugc_season.duration_text, self.style.font.font_size.title)
            await paste(self.canvas, tv, (905, 455))
            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception as e:
            logger.exception(e)
            return None


class DynMajorLive(AbstractMajor):
    async def run(self, repost):
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 695)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        try:
            cover = await get_pictures(f"{self.major.live.cover}@505w_285h_1c.webp", (1010, 570))
            await self.draw_shadow(self.canvas, (35, 25, 1010, 655), 20, background_color)
            rec = skia.Rect.MakeXYWH(35, 25, 1010, 665)
            self.canvas.clipRRect(skia.RRect(rec, 20, 20), skia.ClipOp.kIntersect)
            await self.draw_text(
                self.canvas,
                self.major.live.title,
                self.style.font.font_size.text,
                (60, 650, 980, 600, 10),
                self.style.color.font_color.text,
            )
            await paste(self.canvas, cover, (35, 25))
            if self.major.live.badge is not None and self.major.live.badge.text != "":
                tag = self.major.live.badge.text
            else:
                tag = "投稿视频"
            await self.make_tag(tag, self.style.font.font_size.text)

            await self.make_sub_tag(self.major.live.desc_second, self.style.font.font_size.title)

            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception as e:
            logger.exception(e)
            return None


class DynMajorNone(AbstractMajor):
    async def run(self, repost):
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 100)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        try:
            await self.make_tips()
            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception as e:
            logger.exception(e)
            return None

    async def make_tips(self):
        error = skia.Image.open(path.join(self.src_path, "error.png")).resize(40, 40)
        await self.draw_text(
            self.canvas,
            self.major.none.tips,
            self.style.font.font_size.text,
            (90, 60, 1080, 40, 0),
            self.style.color.font_color.sub_title,
        )
        await paste(self.canvas, error, (40, 30))


class DynMajorBlocked(AbstractMajor):
    async def run(self, repost):
        background_color = self.style.color.background.repost if repost else self.style.color.background.normal
        surface = skia.Surface(1080, 1200)
        self.canvas = surface.getCanvas()
        self.canvas.clear(skia.Color(*background_color))
        try:
            result = await get_pictures(
                [
                    f"{self.major.blocked.bg_img.img_dark}@1c.webp",
                    self.major.blocked.icon.img_day,
                ]
            )
            await self.draw_shadow(self.canvas, (40, 100, 1000, 1000), 20, background_color)
            rec = skia.Rect.MakeXYWH(40, 100, 1000, 1000)
            self.canvas.clipRRect(skia.RRect(rec, 20, 20), skia.ClipOp.kIntersect)
            await paste(self.canvas, result[1], (456, 380))
            await paste(self.canvas, result[0].resize(1000, 1000), (40, 100))
            text = self.major.blocked.hint_message.split("\n")
            await self.draw_text(
                self.canvas,
                text[0],
                self.style.font.font_size.name,
                (380, 630, 980, 600, 10),
                self.style.color.font_color.sub_title,
            )
            await self.draw_text(
                self.canvas,
                text[1],
                self.style.font.font_size.name,
                (160, 700, 980, 600, 10),
                self.style.color.font_color.sub_title,
            )
            return self.canvas.toarray(colorType=skia.ColorType.kRGBA_8888_ColorType)
        except Exception as e:
            logger.exception(e)
            return None
