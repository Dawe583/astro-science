#!/usr/bin/env python3
"""
Convert extract-structure.mjs output to merge-batch-graphs.py expected format.

Input: batch-*-output.json with {results: [...]}
Output: batch-*.json with {nodes: [...], edges: [...]}
"""

import json
import sys
from pathlib import Path


def convert_batch(input_path: Path, output_path: Path):
    with open(input_path, "r") as f:
        data = json.load(f)

    nodes = []
    edges = []

    for result in data.get("results", []):
        path = result.get("path", "")
        language = result.get("language", "")
        file_category = result.get("fileCategory", "")

        # Create file node
        file_id = f"file:{path}"
        nodes.append(
            {
                "id": file_id,
                "type": "file",
                "name": path.split("/")[-1],
                "filePath": path,
                "language": language,
                "fileCategory": file_category,
                "totalLines": result.get("totalLines", 0),
                "nonEmptyLines": result.get("nonEmptyLines", 0),
            }
        )

        # Create function nodes
        for func in result.get("functions", []):
            func_id = f"function:{path}:{func['name']}"
            nodes.append(
                {
                    "id": func_id,
                    "type": "function",
                    "name": func["name"],
                    "filePath": path,
                    "startLine": func.get("startLine", 0),
                    "endLine": func.get("endLine", 0),
                    "params": func.get("params", []),
                }
            )
            edges.append({"source": file_id, "target": func_id, "type": "contains"})

        # Create class nodes
        for cls in result.get("classes", []):
            cls_id = f"class:{path}:{cls['name']}"
            nodes.append(
                {
                    "id": cls_id,
                    "type": "class",
                    "name": cls["name"],
                    "filePath": path,
                    "startLine": cls.get("startLine", 0),
                    "endLine": cls.get("endLine", 0),
                    "methods": cls.get("methods", []),
                    "properties": cls.get("properties", []),
                }
            )
            edges.append({"source": file_id, "target": cls_id, "type": "contains"})

        # Create export nodes
        for exp in result.get("exports", []):
            exp_id = f"export:{path}:{exp['name']}"
            nodes.append(
                {
                    "id": exp_id,
                    "type": "export",
                    "name": exp["name"],
                    "filePath": path,
                    "line": exp.get("line", 0),
                    "isDefault": exp.get("isDefault", False),
                }
            )
            edges.append({"source": file_id, "target": exp_id, "type": "exports"})

        # Create section nodes (for docs/markdown)
        for section in result.get("sections", []):
            sec_id = f"section:{path}:{section['heading']}"
            nodes.append(
                {
                    "id": sec_id,
                    "type": "section",
                    "name": section["heading"],
                    "filePath": path,
                    "level": section.get("level", 1),
                    "line": section.get("line", 0),
                }
            )
            edges.append({"source": file_id, "target": sec_id, "type": "contains"})

        # Create definition nodes
        for defn in result.get("definitions", []):
            def_id = f"definition:{path}:{defn['name']}"
            nodes.append(
                {
                    "id": def_id,
                    "type": "definition",
                    "name": defn["name"],
                    "filePath": path,
                    "kind": defn.get("kind", ""),
                    "fields": defn.get("fields", []),
                    "startLine": defn.get("startLine", 0),
                    "endLine": defn.get("endLine", 0),
                }
            )
            edges.append({"source": file_id, "target": def_id, "type": "contains"})

    output = {"nodes": nodes, "edges": edges}

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(
        f"Converted {input_path} -> {output_path} ({len(nodes)} nodes, {len(edges)} edges)"
    )


def main():
    import glob

    input_dir = Path("/home/dawe/Projects/astro-science/.ua/batch-results")
    output_dir = Path("/home/dawe/Projects/astro-science/.ua/intermediate")

    for input_file in sorted(input_dir.glob("batch-*-output.json")):
        batch_num = input_file.stem.split("-")[1]
        output_file = output_dir / f"batch-{batch_num}.json"
        convert_batch(input_file, output_file)


if __name__ == "__main__":
    main()
