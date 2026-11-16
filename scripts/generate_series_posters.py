import os

posters = {
    "beverly_hillbillies": {
        "title": "BEVERLY HILLBILLIES",
        "sub": "A Família Buscapé • 1962",
        "color1": "#B45309",
        "color2": "#78350F",
        "accent": "#F59E0B",
        "genre": "SÉRIE • COMÉDIA"
    },
    "sherlock_holmes": {
        "title": "SHERLOCK HOLMES",
        "sub": "Ronald Howard • 1954",
        "color1": "#1E293B",
        "color2": "#0F172A",
        "accent": "#38BDF8",
        "genre": "SÉRIE • MISTÉRIO"
    },
    "bonanza": {
        "title": "BONANZA",
        "sub": "Ponderosa Ranch • 1959",
        "color1": "#9A3412",
        "color2": "#431407",
        "accent": "#FB923C",
        "genre": "SÉRIE • FAROESTE"
    },
    "one_step_beyond": {
        "title": "ONE STEP BEYOND",
        "sub": "No Limite da Realidade • 1959",
        "color1": "#4C1D95",
        "color2": "#1E1B4B",
        "accent": "#A855F7",
        "genre": "SÉRIE • SOBRENATURAL"
    },
    "the_lucy_show": {
        "title": "THE LUCY SHOW",
        "sub": "Lucille Ball • 1962",
        "color1": "#BE185D",
        "color2": "#831843",
        "accent": "#F472B6",
        "genre": "SÉRIE • COMÉDIA"
    },
    "robin_hood": {
        "title": "ROBIN HOOD",
        "sub": "Richard Greene • 1955",
        "color1": "#15803D",
        "color2": "#052E16",
        "accent": "#4ADE80",
        "genre": "SÉRIE • AVENTURA"
    },
    "dick_van_dyke": {
        "title": "DICK VAN DYKE",
        "sub": "Carl Reiner • 1961",
        "color1": "#0369A1",
        "color2": "#082F49",
        "accent": "#38BDF8",
        "genre": "SÉRIE • COMÉDIA"
    },
    "dragnet": {
        "title": "DRAGNET",
        "sub": "Sgt. Joe Friday • 1951",
        "color1": "#334155",
        "color2": "#0F172A",
        "accent": "#E2E8F0",
        "genre": "SÉRIE • POLICIAL"
    },
    "flash_gordon": {
        "title": "FLASH GORDON",
        "sub": "Steve Holland • 1954",
        "color1": "#1D4ED8",
        "color2": "#172554",
        "accent": "#60A5FA",
        "genre": "SÉRIE • SCI-FI"
    }
}

os.makedirs('logos', exist_ok=True)

for key, p in posters.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="grad_{key}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{p['color1']}"/>
      <stop offset="100%" stop-color="{p['color2']}"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" rx="48" fill="url(#grad_{key})"/>
  <rect x="20" y="20" width="472" height="472" rx="36" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="4"/>
  
  <!-- Category Badge -->
  <rect x="156" y="56" width="200" height="32" rx="16" fill="{p['accent']}" opacity="0.9"/>
  <text x="256" y="78" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="800" letter-spacing="2" text-anchor="middle">{p['genre']}</text>
  
  <!-- Series Emblem -->
  <circle cx="256" cy="210" r="70" fill="none" stroke="{p['accent']}" stroke-width="6" opacity="0.6"/>
  <circle cx="256" cy="210" r="50" fill="rgba(255,255,255,0.06)"/>
  <polygon points="240,185 285,210 240,235" fill="#FFFFFF"/>
  
  <!-- Title & Subtitle -->
  <text x="256" y="350" fill="#FFFFFF" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="32" font-weight="900" letter-spacing="1" text-anchor="middle">{p['title']}</text>
  <text x="256" y="395" fill="rgba(255,255,255,0.85)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="600" text-anchor="middle">{p['sub']}</text>
  <text x="256" y="440" fill="{p['accent']}" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="700" letter-spacing="3" text-anchor="middle">DOMÍNIO PÚBLICO • VOD</text>
</svg>'''
    
    path = os.path.join('logos', f'poster_{key}.svg')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Generated: {path}")

print("All 9 series poster SVGs generated successfully!")
