# 📦 My COPR Repository

This repository contains spec files for various software packages that I package for Fedora COPR (Cool Other Package Repo).

## 📋 Package List

| Package Name | Description | Version | Original Repository | COPR Link |
|-------------|-------------|---------|-------------------|-----------|
| bustd | A lightweight process killer daemon for out-of-memory scenarios | v0.1.1 | [vrmiguel/bustd](https://github.com/vrmiguel/bustd) | [copr/boobaa/bustd](https://copr.fedorainfracloud.org/coprs/boobaa/bustd/) |

## 💻 Installation

```bash
# Enable a specific package repository
dnf copr enable boobaa/<package-name>

# Install the package
dnf install <package-name>
```

## 🔄 Repository Structure

```
.
├── *.spec        # SPEC files for each package
└── README.md     # This documentation
```

## 🤝 Contributing

Please notify me if:
- A package has a new version release
- You find any package issues
- You have package suggestions

You can reach me via:
- Issues in this repository
- COPR comments

## 📝 Notes

Each package follows its original project's license