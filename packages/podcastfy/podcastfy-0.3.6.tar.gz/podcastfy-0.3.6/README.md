<div align="center">
<a name="readme-top"></a>

# Podcastfy.ai 🎙️🤖
An Open Source API alternative to NotebookLM's podcast feature: Transforming Multimodal Content into Captivating Multilingual Audio Conversations with GenAI

https://github.com/user-attachments/assets/f1559e70-9cf9-4576-b48b-87e7dad1dd0b

[Paper](https://github.com/souzatharsis/podcastfy/blob/main/paper/paper.pdf) |
[Python Package](https://github.com/souzatharsis/podcastfy/blob/59563ee105a0d1dbb46744e0ff084471670dd725/podcastfy.ipynb) |
[CLI](https://github.com/souzatharsis/podcastfy/blob/59563ee105a0d1dbb46744e0ff084471670dd725/usage/cli.md) |
[REST API](https://github.com/souzatharsis/podcastfy/blob/59563ee105a0d1dbb46744e0ff084471670dd725/usage/api.md) |
[Web App](https://huggingface.co/spaces/thatupiso/Podcastfy.ai_demo) |
[Feedback](https://github.com/souzatharsis/podcastfy/issues)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/souzatharsis/podcastfy/blob/main/podcastfy.ipynb)
[![PyPi Status](https://img.shields.io/pypi/v/podcastfy)](https://pypi.org/project/podcastfy/)
![PyPI Downloads](https://static.pepy.tech/badge/podcastfy)
[![Issues](https://img.shields.io/github/issues-raw/souzatharsis/podcastfy)](https://github.com/souzatharsis/podcastfy/issues)
[![Pytest](https://github.com/souzatharsis/podcastfy/actions/workflows/python-app.yml/badge.svg)](https://github.com/souzatharsis/podcastfy/actions/workflows/python-app.yml)
[![Docker](https://github.com/souzatharsis/podcastfy/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/souzatharsis/podcastfy/actions/workflows/docker-publish.yml)
[![Documentation Status](https://readthedocs.org/projects/podcastfy/badge/?version=latest)](https://podcastfy.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![GitHub Repo stars](https://img.shields.io/github/stars/souzatharsis/podcastfy)
</div>

Podcastfy is an open-source Python package that transforms multi-modal content (text, images) into engaging, multi-lingual audio conversations using GenAI. Input content includes websites, PDFs, images, YouTube videos, as well as user provided topics.

Unlike closed-source UI-based tools focused primarily on research synthesis (e.g. NotebookLM ❤️), Podcastfy focuses on open source, programmatic and bespoke generation of engaging, conversational content from a multitude of multi-modal sources, enabling customization and scale.

[![Star History Chart](https://api.star-history.com/svg?repos=souzatharsis/podcastfy&type=Date&theme=dark)](https://api.star-history.com/svg?repos=souzatharsis/podcastfy&type=Date&theme=dark)

## Audio Examples 🔊
This sample collection is also [available at audio.com](https://audio.com/thatupiso/collections/podcastfy).

### Images

| Image Set | Description | Audio |
|:--|:--|:--|
| <img src="data/images/Senecio.jpeg" alt="Senecio, 1922 (Paul Klee)" width="20%" height="auto"> <img src="data/images/connection.jpg" alt="Connection of Civilizations (2017) by Gheorghe Virtosu " width="21.5%" height="auto"> | Senecio, 1922 (Paul Klee) and Connection of Civilizations (2017) by Gheorghe Virtosu  | [<span style="font-size: 25px;">🔊</span>](https://audio.com/thatupiso/audio/output-file-abstract-art) |
| <img src="data/images/japan_1.jpg" alt="The Great Wave off Kanagawa, 1831 (Hokusai)" width="20%" height="auto"> <img src="data/images/japan2.jpg" alt="Takiyasha the Witch and the Skeleton Spectre, c. 1844 (Kuniyoshi)" width="21.5%" height="auto"> | The Great Wave off Kanagawa, 1831 (Hokusai) and Takiyasha the Witch and the Skeleton Spectre, c. 1844 (Kuniyoshi) | [<span style="font-size: 25px;">🔊</span>](https://audio.com/thatupiso/audio/output-file-japan) |
| <img src="data/images/taylor.png" alt="Taylor Swift" width="28%" height="auto"> <img src="data/images/monalisa.jpeg" alt="Mona Lisa" width="10.5%" height="auto"> | Pop culture icon Taylor Swift and Mona Lisa, 1503 (Leonardo da Vinci) | [<span style="font-size: 25px;">🔊</span>](https://audio.com/thatupiso/audio/taylor-monalisa) |

### Text
| Content Type | Description | Audio | Source |
|--------------|-------------|-------|--------|
| Youtube Video | YCombinator on LLMs | [Audio](https://audio.com/thatupiso/audio/ycombinator-llms) | [YouTube](https://www.youtube.com/watch?v=eBVi_sLaYsc) |
| PDF | Book: Networks, Crowds, and Markets | [Audio](https://audio.com/thatupiso/audio/networks) | book pdf |
| Research Paper | Climate Change in France | [Audio](https://audio.com/thatupiso/audio/agro-paper) | [PDF](./data/pdf/s41598-024-58826-w.pdf) |
| Website | My Personal Website | [Audio](https://audio.com/thatupiso/audio/tharsis) | [Website](https://www.souzatharsis.com) |
| Website + YouTube | My Personal Website + YouTube Video on AI | [Audio](https://audio.com/thatupiso/audio/tharsis-ai) | [Website](https://www.souzatharsis.com), [YouTube](https://www.youtube.com/watch?v=sJE1dE2dulg) |

### Multi-Lingual Text
| Language | Content Type | Description | Audio | Source |
|----------|--------------|-------------|-------|--------|
| French | Website | Agroclimate research information | [Audio](https://audio.com/thatupiso/audio/podcast-fr-agro) | [Website](https://agroclim.inrae.fr/) |
| Portuguese-BR | News Article | Election polls in São Paulo | [Audio](https://audio.com/thatupiso/audio/podcast-thatupiso-br) | [Website](https://noticias.uol.com.br/eleicoes/2024/10/03/nova-pesquisa-datafolha-quem-subiu-e-quem-caiu-na-disputa-de-sp-03-10.htm) |

## Features ✨

- Generate conversational content from multiple sources and formats (images, websites, YouTube, and PDFs).
- Generate shorts (2-5 minutes) or longform (30+ minutes) podcasts.
- Customize transcript and audio generation (e.g., style, language, structure).
- Generate transcripts using 100+ LLM models (OpenAI, Anthropic, Google etc).
- Leverage local LLMs for transcript generation for increased privacy and control.
- Integrate with advanced text-to-speech models (OpenAI, Google, ElevenLabs, and Microsoft Edge).
- Provide multi-language support for global content creation.
- Integrate seamlessly with CLI and Python packages for automated workflows.

## Built with Podcastfy 🚀

- [OpenNotebook](https://www.open-notebook.ai/)
- [SurfSense](https://www.surfsense.net/)
- [Podcast-llm](https://github.com/evandempsey/podcast-llm)
- [Podcastfy-HuggingFace App](https://huggingface.co/spaces/thatupiso/Podcastfy.ai_demo)
- [Podcastfy-UI](https://github.com/giulioco/podcastfy-ui)

## Updates 🚀

### v0.3.6+ release
- Generate shorts or longform podcasts!
- Generate podcasts from input topic using real-time internet search
- Integrate with 100+ LLM models (OpenAI, Anthropic, Google etc) for transcript generation
- Integrate with Google's Multispeaker TTS model for high-quality audio generation

See [CHANGELOG](CHANGELOG.md) for more details.

## Quickstart 💻

### Prerequisites
- Python 3.11 or higher
- `$ pip install ffmpeg` (for audio processing)

### Setup
1. Install from PyPI
  `$ pip install podcastfy`

2. Set up your [API keys](usage/config.md)

### Python
```python
from podcastfy.client import generate_podcast

audio_file = generate_podcast(urls=["<url1>", "<url2>"])
```
### CLI
```
python -m podcastfy.client --url <url1> --url <url2>
```
  
## Usage 💻

- [Python Package Quickstart](podcastfy.ipynb)

- [Python Package Reference Manual](https://podcastfy.readthedocs.io/en/latest/podcastfy.html)

- [REST API Reference Manual](usage/api.md)

- [CLI](usage/cli.md)

- [How to](usage/how-to.md)

Experience Podcastfy with our [HuggingFace](https://huggingface.co/spaces/thatupiso/Podcastfy.ai_demo) 🤗 Spaces app. (Note: This UI app is less extensively tested than the Python package.)

## Customization 🔧

Podcastfy offers a range of customization options to tailor your AI-generated podcasts:
- Customize podcast [conversation](usage/conversation_custom.md) (e.g. format, style, voices)
- Choose to run [Local LLMs](usage/local_llm.md) (156+ HuggingFace models)
- Set [System Settings](usage/config_custom.md) (e.g. output directory settings)


## License

This software is licensed under [Apache 2.0](LICENSE). [Here](usage/license-guide.md) are a few instructions if you would like to use podcastfy in your software.

## Contributing 🤝

We welcome contributions! See [Guidelines](GUIDELINES.md) for more details.

## Example Use Cases 🎧🎶

- **Content Creators** can use `Podcastfy` to convert blog posts, articles, or multimedia content into podcast-style audio, enabling them to reach broader audiences. By transforming content into an audio format, creators can cater to users who prefer listening over reading.

- **Educators** can transform lecture notes, presentations, and visual materials into audio conversations, making educational content more accessible to students with different learning preferences. This is particularly beneficial for students with visual impairments or those who have difficulty processing written information.

- **Researchers** can convert research papers, visual data, and technical content into conversational audio. This makes it easier for a wider audience, including those with disabilities, to consume and understand complex scientific information. Researchers can also create audio summaries of their work to enhance accessibility.

- **Accessibility Advocates** can use `Podcastfy` to promote digital accessibility by providing a tool that converts multimodal content into auditory formats. This helps individuals with visual impairments, dyslexia, or other disabilities that make it challenging to consume written or visual content.
  
## Contributors

<a href="https://github.com/souzatharsis/podcastfy/graphs/contributors">
  <img alt="contributors" src="https://contrib.rocks/image?repo=souzatharsis/podcastfy"/>
</a>

<p align="right" style="font-size: 14px; color: #555; margin-top: 20px;">
    <a href="#readme-top" style="text-decoration: none; color: #007bff; font-weight: bold;">
        ↑ Back to Top ↑
    </a>
</p>
