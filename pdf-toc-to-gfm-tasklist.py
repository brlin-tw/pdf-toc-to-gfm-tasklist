#!/usr/bin/env python3
# Extract PDF ToC to GFM task list markup
#
# Copyright 2024 林博仁(Buo-ren, Lin) <buo.ren.lin@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
import PyPDF2

def extract_bookmarks(outlines, level=0):
    bookmarks = []

    for outline in outlines:
        if isinstance(outline, PyPDF2.generic.Destination):
            bookmarks.append((level, outline.title))
        elif isinstance(outline, list):
            # Recursively handle nested bookmarks
            bookmarks.extend(extract_bookmarks(outline, level + 1))

    return bookmarks

def bookmarks_to_gfm_task_list(bookmarks):
    gfm_list = []

    for level, title in bookmarks:
        indent = '  ' * level  # Use two spaces for each level of indentation
        gfm_list.append(f"{indent}* [ ] {title}")

    return "\n".join(gfm_list)

with open("PDF document with ToC.pdf", "rb") as file:
    reader = PyPDF2.PdfFileReader(file)
    outlines = reader.getOutlines()
    bookmarks = extract_bookmarks(outlines)
    gfm_task_list = bookmarks_to_gfm_task_list(bookmarks)

print(gfm_task_list)
