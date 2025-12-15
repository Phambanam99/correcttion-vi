from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import datetime


def _get_or_create_comments_part(document_part):
    """
    Tạo comments part nếu chưa có (tương thích python-docx >= 1.1)
    """
    if hasattr(document_part, "_comments_part") and document_part._comments_part:
        return document_part._comments_part

    return document_part._add_comments_part()


def _get_next_comment_id(comments_part):
    """
    Lấy comment_id tiếp theo bằng cách đếm comment hiện có
    (CÁCH ĐÚNG – không dùng private attribute)
    """
    existing_ids = [
        int(c.get(qn("w:id")))
        for c in comments_part._element.findall(qn("w:comment"))
        if c.get(qn("w:id")) is not None
    ]
    return max(existing_ids, default=-1) + 1


def add_comment(paragraph, text, author):
    part = paragraph.part
    comments_part = _get_or_create_comments_part(part)

    comment_id = _get_next_comment_id(comments_part)

    # Tạo comment
    comment = OxmlElement("w:comment")
    comment.set(qn("w:id"), str(comment_id))
    comment.set(qn("w:author"), author)
    comment.set(qn("w:date"), datetime.datetime.utcnow().isoformat())

    p = OxmlElement("w:p")
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = text

    r.append(t)
    p.append(r)
    comment.append(p)

    comments_part._element.append(comment)

    # Gắn comment vào paragraph
    p_elm = paragraph._p

    start = OxmlElement("w:commentRangeStart")
    start.set(qn("w:id"), str(comment_id))

    end = OxmlElement("w:commentRangeEnd")
    end.set(qn("w:id"), str(comment_id))

    ref = OxmlElement("w:r")
    ref_mark = OxmlElement("w:commentReference")
    ref_mark.set(qn("w:id"), str(comment_id))
    ref.append(ref_mark)

    p_elm.insert(0, start)
    p_elm.append(end)
    p_elm.append(ref)
