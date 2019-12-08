name: Build DrumBurp
on:
  push:
    tags:
      - "*.*.*"

jobs:
  create_release:
    name: Create Release
    runs-on: ubuntu-latest
    steps:
      - name: Create Release
        id: this-release
        uses: actions/create-release@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
  build_windows:
    needs: create_release
    name: Windows
    runs-on: windows-2019
    steps:
      - name: Checkout
        uses: actions/checkout@master
      - name: Python Setup
        uses: actions/setup-python@v1
        with:
          python-version: "2.7.16"
          architecture: "x64"
      - name: Install
        run: build/install_windows.ps1
      - name: Build
        run: build/build_windows.ps1
      - name: Upload to Release
        uses: actions/upload-release-asset@v1.0.1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ jobs.create_release.this-release.outputs.upload_url }}
          asset_path: "build/output/*.exe"
          asset_content_type: application/octet-stream
  build_linux:
    needs: create_release
    name: Linux
    runs=on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@master
      - name: Python Setup
        uses: actions/setup-python@v1
        with:
          python-version: "2.7.16"
          architecture: "x64"
      - name: Install
        run: build/install_linux.sh
      - name: Build
        run: build/build_linux.sh
      - name: Upload to Release
        uses: actions/upload-release-asset@v1.0.1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          upload_url: ${{ jobs.create_release.this-release.outputs.upload_url }}
          asset_path: "build/output/DrumBurp"
          asset_content_type: application/octet-stream
