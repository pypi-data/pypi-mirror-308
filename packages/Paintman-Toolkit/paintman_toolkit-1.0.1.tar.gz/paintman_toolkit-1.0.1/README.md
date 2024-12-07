# PaintmanToolkit

**PaintmanToolkit** is a comprehensive Python module designed for managing Paintman CCF (Color Chart File) and CRF (Color Replace File) formats, essential for color chart and replacement management in animation production. The toolkit supports reading and generating files with both 8-bit and 16-bit RGB(only for CCFReader) color depths.

## Installation

To install PaintmanToolkit, use `pip`:

```bash
pip install PaintmanToolkit
```

## Usage

### Importing the Module
```python
from PaintmanToolkit import CCFGenerator, CCFReader, CRFReader, CRFGenerator, RGB8, RGB16
```

---

### Working with CCF Files

#### Creating a CCF File
Use `CCFGenerator` to create a CCF file:

```python
color_data = [
    ((255, 0, 0), "Red"),
    ((0, 255, 0), "Green"),
    ((0, 0, 255), "Blue峠"),  # Example with Japanese characters
    ((0, 0, 0), "黑色辻"),  # Example with Chinese characters
    ((255, 255, 255), "White白色"),  # Example with mixed characters
    ((128, 128, 128), "Gray灰色"),
    ((255, 255, 0), "Yellow"),
    ((0, 255, 255), "Cyanシアン"),  # Japanese characters
    ((255, 0, 255), "Magenta")
]

generator = CCFGenerator(color_data)
generator.create_ccf_file("output_file.ccf")
print("CCF file created successfully at 'output_file.ccf'")
```

#### Reading a CCF File
Use `CCFReader` to read a CCF file:

```python
reader = CCFReader("output_file.ccf")

# Reading with 8-bit RGB
color_data_8bit = reader.read_ccf_file(RGB8)
print("8-bit RGB Color Data:")
for label, rgb in color_data_8bit:
    print(f"Label: {label}, RGB: {rgb}")

# Reading with 16-bit RGB
color_data_16bit = reader.read_ccf_file(RGB16)
print("\n16-bit RGB Color Data:")
for label, rgb in color_data_16bit:
    print(f"Label: {label}, RGB: {rgb}")
```

---

### Working with CRF Files

#### Reading a CRF File
Use `CRFReader` to read a CRF file:

```python
reader = CRFReader()
color_pairs = reader.read_crf_file("input_file.crf")
print("CRF Color Pairs:")
for color1, color2 in color_pairs:
    print(f"Color 1: {color1}, Color 2: {color2}")
```

#### Creating a CRF File
Use `CRFGenerator` to generate a CRF file:

```python
color_pairs = [
    [(0, 0, 0), (205, 246, 225)],
    [(40, 38, 37), (10, 16, 36)],
    # Add more color pairs as needed
]

generator = CRFGenerator()
generator.generate_crf_file(color_pairs, "output_file.crf")
print("CRF file created successfully at 'output_file.crf'")
```

---

## Constants

- `RGB8`: Constant for 8-bit RGB color depth.
- `RGB16`: Constant for 16-bit RGB color depth.

---

## Exception Handling

- **CCFGenerator** raises a `ValueError` if any RGB value exceeds 255, ensuring values are valid 8-bit RGB before encoding.
- **CRFGenerator** raises a `ValueError` if the color pairs list is empty or exceeds 256 pairs.

---

## Important Notes

- **CCF Files**: `CCFGenerator` currently does not support 16-bit RGB or RGBA encoding.
- **CRF Files**: `CRFGenerator` ensures a maximum of 256 color pairs and fills with white pairs if the count is less than 123.

---

## License

This project is licensed under the MIT License.

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to suggest improvements or report bugs.

---

## Contact

For questions or support, feel free to submit a pull request or open an issue.

Enjoy using **PaintmanToolkit** for your color chart and color replacement management in animation projects!
