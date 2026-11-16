import json
import os
import urllib.parse

# 30 Live Public & Educational Channels mapped by Country
LIVE_CHANNELS_DATA = [
    # Brasil (10)
    {
        "id": "TVBrasil.br",
        "name_pt": "TV Brasil (EBC)",
        "name_en": "TV Brasil (EBC National Public TV)",
        "country": "BR",
        "country_pt": "Brasil",
        "country_en": "Brazil",
        "lang": "pt-BR",
        "url": "https://tvbrasil-stream.ebc.com.br/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Logotipo_da_TV_Brasil.svg/512px-Logotipo_da_TV_Brasil.svg.png",
        "ref_logo": "logos/tv_brasil.svg",
        "desc_pt": "Emissora pública da Empresa Brasil de Comunicação (EBC). Conteúdo cultural, educativo e jornalístico gratuito.",
        "desc_en": "Brazil's national public broadcaster operated by EBC. Cultural, educational, and news programming."
    },
    {
        "id": "CanalGov.br",
        "name_pt": "Canal Gov (EBC)",
        "name_en": "Canal Gov (Brazil Government TV)",
        "country": "BR",
        "country_pt": "Brasil",
        "country_en": "Brazil",
        "lang": "pt-BR",
        "url": "https://canalgov-stream.ebc.com.br/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Logotipo_do_Canal_Gov.svg/512px-Logotipo_do_Canal_Gov.svg.png",
        "ref_logo": "logos/canal_gov.svg",
        "desc_pt": "Canal de televisão governamental sob gestão da EBC. Transmissão pública de utilidade pública e educação cívica.",
        "desc_en": "Official government television operated by EBC. Civic education and public affairs."
    },
    {
        "id": "CulturaFast.br",
        "name_pt": "TV Cultura",
        "name_en": "TV Cultura (Padre Anchieta Foundation)",
        "country": "BR",
        "country_pt": "Brasil",
        "country_en": "Brazil",
        "lang": "pt-BR",
        "url": "https://fpa-gateway.tvcultura.com.br:8181/memfs/606caef0-a290-413d-9f1f-8fcdb3a73831.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Logo_TV_Cultura_2020.svg/512px-Logo_TV_Cultura_2020.svg.png",
        "ref_logo": "logos/tv_cultura.svg",
        "desc_pt": "Fundação Padre Anchieta. A mais premiada emissora educativa e cultural da televisão pública brasileira.",
        "desc_en": "Padre Anchieta Foundation. Brazil's award-winning educational and cultural public broadcaster."
    },
    {
        "id": "TVSenado.br",
        "name_pt": "TV Senado",
        "name_en": "TV Senado (Federal Senate of Brazil)",
        "country": "BR",
        "country_pt": "Brasil",
        "country_en": "Brazil",
        "lang": "pt-BR",
        "url": "http://170.83.16.50/TV_SENADO/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/TV_Senado_logo.svg/512px-TV_Senado_logo.svg.png",
        "ref_logo": "logos/tv_senado.svg",
        "desc_pt": "Canal legislativo oficial aberto do Senado Federal do Brasil. Transmissões de sessões e documentários culturais.",
        "desc_en": "Official parliamentary channel of the Brazilian Federal Senate. Live debates and cultural documentaries."
    },
    {
        "id": "TVCamara.br",
        "name_pt": "TV Câmara",
        "name_en": "TV Câmara (Chamber of Deputies of Brazil)",
        "country": "BR",
        "country_pt": "Brasil",
        "country_en": "Brazil",
        "lang": "pt-BR",
        "url": "https://stream3.camara.gov.br/tv1/manifest.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Logo_TV_C%C3%A2mara.svg/512px-Logo_TV_C%C3%A2mara.svg.png",
        "ref_logo": "logos/tv_camara.svg",
        "desc_pt": "Canal oficial aberto da Câmara dos Deputados do Brasil. Plenário, comissões e programas culturais públicos.",
        "desc_en": "Official parliamentary channel of the Brazilian Chamber of Deputies."
    },
    {
        "id": "TVJustica.br",
        "name_pt": "TV Justiça",
        "name_en": "TV Justiça (Supreme Federal Court of Brazil)",
        "country": "BR",
        "country_pt": "Brasil",
        "country_en": "Brazil",
        "lang": "pt-BR",
        "url": "http://170.83.16.50/TV_JUSTICA/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Logo_TV_Justi%C3%A7a.png/512px-Logo_TV_Justi%C3%A7a.png",
        "ref_logo": "logos/tv_justica.svg",
        "desc_pt": "Canal público coordenado pelo Supremo Tribunal Federal (STF). Julgamentos ao vivo e debates jurídicos.",
        "desc_en": "Public judicial channel coordinated by Brazil's Supreme Court (STF). Live court proceedings."
    },
    {
        "id": "CanalEducacao.br",
        "name_pt": "Canal Educação (MEC / EBC)",
        "name_en": "Canal Educação (Ministry of Education / EBC)",
        "country": "BR",
        "country_pt": "Brasil",
        "country_en": "Brazil",
        "lang": "pt-BR",
        "url": "https://canaleducacao-stream.ebc.com.br/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Canal_Educa%C3%A7%C3%A3o_logo_2023.png/512px-Canal_Educa%C3%A7%C3%A3o_logo_2023.png",
        "ref_logo": "logos/canal_educacao.svg",
        "desc_pt": "Canal oficial educativo do Ministério da Educação (MEC) gerido pela EBC.",
        "desc_en": "Official educational television channel of the Brazilian Ministry of Education."
    },
    {
        "id": "CanalFutura.br",
        "name_pt": "Canal Futura",
        "name_en": "Canal Futura (Educational Public TV)",
        "country": "BR",
        "country_pt": "Brasil",
        "country_en": "Brazil",
        "lang": "pt-BR",
        "url": "http://170.83.16.50/FUTURA/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/d/d4/Logotipo_do_Canal_Futura.png/512px-Logotipo_do_Canal_Futura.png",
        "ref_logo": "logos/canal_futura.svg",
        "desc_pt": "Projeto de comunicação comunitária e educativa pioneiro no Brasil.",
        "desc_en": "Pioneering community and educational television in Brazil."
    },
    {
        "id": "TVEBahia.br",
        "name_pt": "TVE Bahia (IRDEB)",
        "name_en": "TVE Bahia (Bahia Public Broadcaster)",
        "country": "BR",
        "country_pt": "Brasil",
        "country_en": "Brazil",
        "lang": "pt-BR",
        "url": "http://streaming.procergs.com.br:1935/tve/stve/playlist.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Logo_TVE_Bahia_2017.png/512px-Logo_TVE_Bahia_2017.png",
        "ref_logo": "logos/tve_bahia.svg",
        "desc_pt": "Emissora pública educativa do Instituto de Radiodifusão Educativa da Bahia.",
        "desc_en": "Educational public broadcaster of the State of Bahia (IRDEB)."
    },
    {
        "id": "CulturaPara.br",
        "name_pt": "TV Cultura do Pará (FUNTELPA)",
        "name_en": "TV Cultura Pará (Amazonian Public TV)",
        "country": "BR",
        "country_pt": "Brasil",
        "country_en": "Brazil",
        "lang": "pt-BR",
        "url": "http://www.portalcultura.com.br/playerhtml/funtelpa/tv_funtelpa/playlist.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/9/90/TV_Cultura_do_Par%C3%A1_logo.png/512px-TV_Cultura_do_Par%C3%A1_logo.png",
        "ref_logo": "logos/cultura_para.svg",
        "desc_pt": "Fundação Paraense de Radiodifusão (FUNTELPA). Emissora pública e cultural do Pará.",
        "desc_en": "Public and cultural television of Pará state in the Amazon region."
    },

    # Portugal & Europa (6)
    {
        "id": "ARTV.pt",
        "name_pt": "ARTV - Canal Parlamento (Portugal)",
        "name_en": "ARTV - Parliament Channel (Portugal)",
        "country": "PT",
        "country_pt": "Portugal & Europa",
        "country_en": "Portugal & Europe",
        "lang": "pt-PT",
        "url": "https://playout172.livextend.cloud/liveiframe/_definst_/liveartvabr/playlist.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/pt/thumb/2/29/Canal_Parlamento.png/512px-Canal_Parlamento.png",
        "ref_logo": "logos/artv_portugal.svg",
        "desc_pt": "Canal oficial de transmissão pública da Assembleia da República de Portugal.",
        "desc_en": "Official public television channel of the Parliament of the Portuguese Republic."
    },
    {
        "id": "EuronewsPortuguese.fr",
        "name_pt": "Euronews (Edição em Português)",
        "name_en": "Euronews (Portuguese Edition)",
        "country": "EU",
        "country_pt": "Portugal & Europa",
        "country_en": "Portugal & Europe",
        "lang": "pt",
        "url": "https://cdn-euronews.akamaized.net/live/eds/euronews-pt/25040/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Euronews_logo_2016.svg/512px-Euronews_logo_2016.svg.png",
        "ref_logo": "logos/euronews_pt.svg",
        "desc_pt": "Sinal internacional de notícias pan-europeu gratuito e aberto com locução em português.",
        "desc_en": "Pan-European multilingual international news network in Portuguese."
    },
    {
        "id": "CanalParlamento.es",
        "name_pt": "Canal Parlamento (Espanha)",
        "name_en": "Canal Parlamento (Spain Congress of Deputies)",
        "country": "ES",
        "country_pt": "Portugal & Europa",
        "country_en": "Portugal & Europe",
        "lang": "es",
        "url": "https://congresodirecto.akamaized.net/hls/live/2037973/canalparlamento/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Logo_Congreso_de_los_Diputados.svg/512px-Logo_Congreso_de_los_Diputados.svg.png",
        "ref_logo": "logos/canal_parlamento_es.svg",
        "desc_pt": "Emissão oficial aberta do Congresso dos Deputados do Reino de Espanha.",
        "desc_en": "Official parliamentary live broadcast of the Congress of Deputies of Spain."
    },
    {
        "id": "ARDalpha.de",
        "name_pt": "ARD-alpha (Alemanha)",
        "name_en": "ARD-alpha (German Science & Educational TV)",
        "country": "DE",
        "country_pt": "Portugal & Europa",
        "country_en": "Portugal & Europe",
        "lang": "de",
        "url": "https://mcdn.br.de/br/fs/ard_alpha/hls/de/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/ARD-alpha_2019.svg/512px-ARD-alpha_2019.svg.png",
        "ref_logo": "logos/ard_alpha.svg",
        "desc_pt": "O canal de televisão público alemão de ciência, educação e alta cultura da rede ARD.",
        "desc_en": "German public television channel dedicated to science, education and culture (ARD network)."
    },
    {
        "id": "SenatoTV.it",
        "name_pt": "Senato TV (Itália)",
        "name_en": "Senato TV (Senate of the Republic of Italy)",
        "country": "IT",
        "country_pt": "Portugal & Europa",
        "country_en": "Portugal & Europe",
        "lang": "it",
        "url": "https://senato-live.morescreens.com/SENATO_1_001/playlist.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Logo_Senato_della_Repubblica.svg/512px-Logo_Senato_della_Repubblica.svg.png",
        "ref_logo": "logos/senato_tv_it.svg",
        "desc_pt": "Transmissão parlamentar oficial aberta do Senado da República Italiana.",
        "desc_en": "Official live parliamentary proceedings of the Italian Senate."
    },
    {
        "id": "CameradeiDeputati.it",
        "name_pt": "Camera dei Deputati (Itália)",
        "name_en": "Camera dei Deputati (Chamber of Deputies of Italy)",
        "country": "IT",
        "country_pt": "Portugal & Europa",
        "country_en": "Portugal & Europe",
        "lang": "it",
        "url": "https://video-ar.radioradicale.it/diretta/camera2/playlist.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Emblem_of_the_Chamber_of_Deputies_%28Italy%29.svg/512px-Emblem_of_the_Chamber_of_Deputies_%28Italy%29.svg.png",
        "ref_logo": "logos/camera_deputati_it.svg",
        "desc_pt": "Transmissão oficial ao vivo da Câmara dos Deputados do Parlamento Italiano.",
        "desc_en": "Official live broadcast of the Italian Chamber of Deputies."
    },

    # América Latina (7)
    {
        "id": "SenalColombia.co",
        "name_pt": "Señal Colombia",
        "name_en": "Señal Colombia (Colombia National Public TV)",
        "country": "CO",
        "country_pt": "América Latina",
        "country_en": "Latin America",
        "lang": "es",
        "url": "http://138.121.15.230:9002/SENAL-COLOMBIA/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Se%C3%B1al_Colombia_logo.svg/512px-Se%C3%B1al_Colombia_logo.svg.png",
        "ref_logo": "logos/senal_colombia.svg",
        "desc_pt": "Emissora de televisão pública nacional educativa e cultural da Colômbia (RTVC).",
        "desc_en": "National educational and cultural public television channel of Colombia (RTVC)."
    },
    {
        "id": "CanalInstitucional.co",
        "name_pt": "Canal Institucional (Colômbia)",
        "name_en": "Canal Institucional (Colombia State TV)",
        "country": "CO",
        "country_pt": "América Latina",
        "country_en": "Latin America",
        "lang": "es",
        "url": "http://190.61.47.54:8000/play/a00v/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Canal_Institucional_logo_2018.png/512px-Canal_Institucional_logo_2018.png",
        "ref_logo": "logos/canal_institucional_co.svg",
        "desc_pt": "Canal estatal da Colômbia dedicado a informar a cidadania sobre o Estado e serviços públicos.",
        "desc_en": "State television channel of Colombia dedicated to civic information and public services."
    },
    {
        "id": "CanalCongreso.co",
        "name_pt": "Canal Congreso (Colômbia)",
        "name_en": "Canal Congreso (Congress of Colombia)",
        "country": "CO",
        "country_pt": "América Latina",
        "country_en": "Latin America",
        "lang": "es",
        "url": "http://138.121.15.230:9002/CANAL-CONGRESO/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Logo_del_Congreso_de_la_Rep%C3%BAblica_de_Colombia.png/512px-Logo_del_Congreso_de_la_Rep%C3%BAblica_de_Colombia.png",
        "ref_logo": "logos/canal_congreso_co.svg",
        "desc_pt": "Canal institucional oficial do Congresso da República da Colômbia.",
        "desc_en": "Official institutional broadcast of the Congress of the Republic of Colombia."
    },
    {
        "id": "TVSenado.cl",
        "name_pt": "TV Senado (Chile)",
        "name_en": "TV Senado (Senate of Chile)",
        "country": "CL",
        "country_pt": "América Latina",
        "country_en": "Latin America",
        "lang": "es",
        "url": "https://janus-tv-ply.senado.cl/playlist/playlist.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Logo_Senado_de_Chile.svg/512px-Logo_Senado_de_Chile.svg.png",
        "ref_logo": "logos/tv_senado_cl.svg",
        "desc_pt": "Canal oficial aberto de televisão do Senado da República do Chile.",
        "desc_en": "Official parliamentary television channel of the Senate of Chile."
    },
    {
        "id": "TVPeru.pe",
        "name_pt": "TV Perú",
        "name_en": "TV Perú (National Public Broadcaster)",
        "country": "PE",
        "country_pt": "América Latina",
        "country_en": "Latin America",
        "lang": "es",
        "url": "http://181.224.200.5:2277/play/a0dx/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/TV_Per%C3%BA_logo_2019.png/512px-TV_Per%C3%BA_logo_2019.png",
        "ref_logo": "logos/tv_peru.svg",
        "desc_pt": "A mais antiga emissora pública do Peru, pertencente ao Instituto Nacional de Radio y Televisión.",
        "desc_en": "Peru's oldest public broadcaster operated by IRTP."
    },
    {
        "id": "CanalIPe.pe",
        "name_pt": "Canal IPe (Peru)",
        "name_en": "Canal IPe (Peru Cultural & Children's Public TV)",
        "country": "PE",
        "country_pt": "América Latina",
        "country_en": "Latin America",
        "lang": "es",
        "url": "http://187.102.210.46/IPE/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Canal_IPe_logo_2020.png/512px-Canal_IPe_logo_2020.png",
        "ref_logo": "logos/canal_ipe_pe.svg",
        "desc_pt": "Canal público cultural e infanto-juvenil do Ministério da Educação do Peru.",
        "desc_en": "Cultural and youth public television channel of Peru's Ministry of Education."
    },
    {
        "id": "Cultura24.pe",
        "name_pt": "Cultura 24 (Peru)",
        "name_en": "Cultura 24 (Peru Ministry of Culture)",
        "country": "PE",
        "country_pt": "América Latina",
        "country_en": "Latin America",
        "lang": "es",
        "url": "https://www.opencaster.com/resources/hls_stream/cultura24.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Escudo_nacional_del_Per%C3%BA.svg/512px-Escudo_nacional_del_Per%C3%BA.svg.png",
        "ref_logo": "logos/cultura_24_pe.svg",
        "desc_pt": "Canal audiovisual oficial de difusão de patrimônio e artes do Ministério da Cultura do Peru.",
        "desc_en": "Official arts and heritage channel of the Ministry of Culture of Peru."
    },

    # Estados Unidos & Global (4)
    {
        "id": "UNWebTV.us",
        "name_pt": "UN Web TV (Nações Unidas)",
        "name_en": "UN Web TV (United Nations Global Webcast)",
        "country": "UN",
        "country_pt": "Estados Unidos & Global",
        "country_en": "United States & Global",
        "lang": "multilingual",
        "url": "https://cdnapi.kaltura.com/p/2503451/sp/250345100/playManifest/entryId/1_gb6tjmle/protocol/https/format/applehttp/a.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Flag_of_the_United_Nations.svg/512px-Flag_of_the_United_Nations.svg.png",
        "ref_logo": "logos/un_web_tv.svg",
        "desc_pt": "Canal oficial internacional da Organização das Nações Unidas (ONU) transmitindo assembleias e direitos humanos.",
        "desc_en": "Official global webcast of the United Nations covering General Assembly and Human Rights councils."
    },
    {
        "id": "ClassicArtsShowcase.us",
        "name_pt": "Classic Arts Showcase",
        "name_en": "Classic Arts Showcase (Public Domain Arts & Opera)",
        "country": "US",
        "country_pt": "Estados Unidos & Global",
        "country_en": "United States & Global",
        "lang": "en",
        "url": "https://classicarts.akamaized.net/hls/live/1024257/CAS/master.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Classic_Arts_Showcase_logo.png/512px-Classic_Arts_Showcase_logo.png",
        "ref_logo": "logos/classic_arts_showcase.svg",
        "desc_pt": "Canal 24/7 de fomento cultural gratuito: concertos clássicos, óperas, balés e acervos de domínio público.",
        "desc_en": "24/7 non-commercial arts channel showcasing classical concerts, opera, ballet, and public domain clips."
    },
    {
        "id": "Create.us",
        "name_pt": "Create TV (PBS)",
        "name_en": "Create TV (PBS Educational Network)",
        "country": "US",
        "country_pt": "Estados Unidos & Global",
        "country_en": "United States & Global",
        "lang": "en",
        "url": "https://create.lls.pbs.org/index.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Create_TV_logo.svg/512px-Create_TV_logo.svg.png",
        "ref_logo": "logos/create_tv.svg",
        "desc_pt": "Rede pública americana educativa (PBS) dedicada a artes, culinária, pintura e sustentabilidade.",
        "desc_en": "American public educational television network (PBS) focused on arts, culinary, painting, and do-it-yourself."
    },
    {
        "id": "DistrictofColumbiaNetwork.us",
        "name_pt": "DCN - District of Columbia Network",
        "name_en": "DCN (Washington D.C. Capital Network)",
        "country": "US",
        "country_pt": "Estados Unidos & Global",
        "country_en": "United States & Global",
        "lang": "en",
        "url": "https://video.oct.dc.gov/out/u/DCN.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Flag_of_the_District_of_Columbia.svg/512px-Flag_of_the_District_of_Columbia.svg.png",
        "ref_logo": "logos/dcn_washington.svg",
        "desc_pt": "Canal público governamental e de transparência cívica da capital dos Estados Unidos (Washington D.C.).",
        "desc_en": "Civic television network of the government of Washington D.C."
    },

    # Ásia & Internacional (3)
    {
        "id": "NHKWorldJapan.jp",
        "name_pt": "NHK World-Japan",
        "name_en": "NHK World-Japan (International Public TV)",
        "country": "JP",
        "country_pt": "Ásia",
        "country_en": "Asia",
        "lang": "en",
        "url": "https://freem3u.xyz/api/live/play.m3u8?vid=106",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/NHK_World-Japan_logo_2020.svg/512px-NHK_World-Japan_logo_2020.svg.png",
        "ref_logo": "logos/nhk_world.svg",
        "desc_pt": "Transmissão internacional pública aberta do Japão (NHK) com notícias globais e documentários sobre ciência e cultura.",
        "desc_en": "Japan's international public broadcasting service (NHK) in English."
    },
    {
        "id": "KTV.kr",
        "name_pt": "KTV - Korea Policy TV",
        "name_en": "KTV (Korea National Policy Television)",
        "country": "KR",
        "country_pt": "Ásia",
        "country_en": "Asia",
        "lang": "ko",
        "url": "https://hlive.ktv.go.kr/live/klive_h.stream/playlist.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Flag_of_South_Korea.svg/512px-Flag_of_South_Korea.svg.png",
        "ref_logo": "logos/ktv_korea.svg",
        "desc_pt": "Canal oficial público de políticas públicas, história nacional e cidadania da Coreia do Sul.",
        "desc_en": "South Korea's public service television covering national policy, heritage, and civic life."
    },
    {
        "id": "ArirangTV.kr",
        "name_pt": "Arirang TV",
        "name_en": "Arirang TV (Korea International Culture)",
        "country": "KR",
        "country_pt": "Ásia",
        "country_en": "Asia",
        "lang": "en",
        "url": "https://dash3.antik.sk/live/test_arirang/playlist.m3u8",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Arirang_TV_logo.svg/512px-Arirang_TV_logo.svg.png",
        "ref_logo": "logos/arirang_tv.svg",
        "desc_pt": "Emissora internacional pública em língua inglesa sediada em Seul, com foco em cultura, cooperação e artes.",
        "desc_en": "English-language international public network based in Seoul promoting Korean culture and international affairs."
    }
]

SERIES_DATA = [
    # 1. A Família Buscapé (The Beverly Hillbillies) - 1962
    {
        "id": "ep_beverly_hillbillies_s01e01",
        "series_id": "beverly_hillbillies",
        "title_pt": "A Família Buscapé S01E01 - Os Clampetts Descobrem Petróleo",
        "title_en": "The Beverly Hillbillies S01E01 - The Clampetts Strike Oil",
        "year": 1962,
        "group_pt": "Séries | Comédia Clássica",
        "group_en": "Series | Classic Comedy",
        "creator": "Paul Henning",
        "lang": "en",
        "stream_url": "https://archive.org/download/Beverly_Hillbillies_Ep01_The_Clampetts_Strike_Oil/BH01_The_Clampetts_Strike_Oil_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_beverly_hillbillies.svg",
        "desc_pt": "Clássica comédia da TV sobre a família caipira Clampett que enriquece ao encontrar petróleo em suas terras e se muda para Beverly Hills.",
        "desc_en": "Classic American sitcom following the Clampett family who strike oil on their land and relocate to Beverly Hills.",
        "size_mb": 103.3
    },
    {
        "id": "ep_beverly_hillbillies_s01e02",
        "series_id": "beverly_hillbillies",
        "title_pt": "A Família Buscapé S01E02 - Instalando-se na Mansão",
        "title_en": "The Beverly Hillbillies S01E02 - Getting Settled",
        "year": 1962,
        "group_pt": "Séries | Comédia Clássica",
        "group_en": "Series | Classic Comedy",
        "creator": "Paul Henning",
        "lang": "en",
        "stream_url": "https://archive.org/download/thebeverlyhillbilliesgettingsettledhq/The Beverly Hillbillies - Getting Settled HQ.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_beverly_hillbillies.svg",
        "desc_pt": "Os Clampetts chegam à sua nova mansão e confundem os luxos modernos com ferramentas de fazenda.",
        "desc_en": "The Clampetts arrive at their new mansion and mistake modern luxuries for farm equipment.",
        "size_mb": 155.1
    },
    {
        "id": "ep_beverly_hillbillies_s01e06",
        "series_id": "beverly_hillbillies",
        "title_pt": "A Família Buscapé S01E06 - Travessuras ou Gostosuras",
        "title_en": "The Beverly Hillbillies S01E06 - Trick Or Treat",
        "year": 1962,
        "group_pt": "Séries | Comédia Clássica",
        "group_en": "Series | Classic Comedy",
        "creator": "Paul Henning",
        "lang": "en",
        "stream_url": "https://archive.org/download/Beverly_Hillbillies_Ep06_Trick_Or_Treat/BH06_Trick_Or_Treat_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_beverly_hillbillies.svg",
        "desc_pt": "No Halloween, os Clampetts acreditam que as crianças fantasiadas são criaturas reais necessitando de ajuda.",
        "desc_en": "On Halloween, the Clampetts think costume-wearing neighbors are in genuine need.",
        "size_mb": 104.8
    },
    {
        "id": "ep_beverly_hillbillies_s01e07",
        "series_id": "beverly_hillbillies",
        "title_pt": "A Família Buscapé S01E07 - Os Criados",
        "title_en": "The Beverly Hillbillies S01E07 - The Servants",
        "year": 1962,
        "group_pt": "Séries | Comédia Clássica",
        "group_en": "Series | Classic Comedy",
        "creator": "Paul Henning",
        "lang": "en",
        "stream_url": "https://archive.org/download/Beverly_Hillbillies_Ep07_The_Servants/BH07_The_Servants_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_beverly_hillbillies.svg",
        "desc_pt": "O banqueiro Drysdale envia criados para ajudar a família, gerando confusões cômicas impagáveis.",
        "desc_en": "Mr. Drysdale hires refined domestic servants for the Clampetts, causing hilarious misunderstandings.",
        "size_mb": 103.9
    },

    # 2. Sherlock Holmes (1954 TV Series)
    {
        "id": "ep_sherlock_holmes_s01e08",
        "series_id": "sherlock_holmes",
        "title_pt": "Sherlock Holmes S01E08 - O Caso da Múmia que Ri",
        "title_en": "Sherlock Holmes S01E08 - The Case of the Laughing Mummy",
        "year": 1954,
        "group_pt": "Séries | Mistério & Policial",
        "group_en": "Series | Mystery & Crime",
        "creator": "Sheldon Reynolds / Ronald Howard",
        "lang": "en",
        "stream_url": "https://archive.org/download/Sherlock_Holmes_TCOT_Laughing_Mummy/TheCaseOfTheLaughingMummy.ia.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_sherlock_holmes.svg",
        "desc_pt": "Sherlock Holmes e Dr. Watson investigam uma relíquia egípcia antiga que supostamente emite gargalhadas misteriosas.",
        "desc_en": "Holmes and Watson investigate an ancient Egyptian mummy that allegedly produces eerie laughing sounds.",
        "size_mb": 147.3
    },
    {
        "id": "ep_sherlock_holmes_s01e10",
        "series_id": "sherlock_holmes",
        "title_pt": "Sherlock Holmes S01E10 - O Caso da Filha do Tirano",
        "title_en": "Sherlock Holmes S01E10 - The Case of the Tyrant's Daughter",
        "year": 1954,
        "group_pt": "Séries | Mistério & Policial",
        "group_en": "Series | Mystery & Crime",
        "creator": "Sheldon Reynolds / Ronald Howard",
        "lang": "en",
        "stream_url": "https://archive.org/download/SherlockHolmes-TheCaseOfTheTyrantsDaughter/TyrantsDaughter_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_sherlock_holmes.svg",
        "desc_pt": "Um cientista autoritário é envenenado e sua noiva é acusada; Holmes desvenda o verdadeiro culpado.",
        "desc_en": "A tyrannical scientist is poisoned, and his fiancée is framed until Holmes intervenes.",
        "size_mb": 112.0
    },
    {
        "id": "ep_sherlock_holmes_s01e11",
        "series_id": "sherlock_holmes",
        "title_pt": "Sherlock Holmes S01E11 - O Caso do Pudim de Natal",
        "title_en": "Sherlock Holmes S01E11 - The Case of the Christmas Pudding",
        "year": 1955,
        "group_pt": "Séries | Mistério & Policial",
        "group_en": "Series | Mystery & Crime",
        "creator": "Sheldon Reynolds / Ronald Howard",
        "lang": "en",
        "stream_url": "https://archive.org/download/sherlock-holmes-the-case-of-the-christmas-pudding-1955-christmas-mystery/Sherlock Holmes - The Case of the Christmas Pudding (1955 Christmas, Mystery).mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_sherlock_holmes.svg",
        "desc_pt": "Um assassino condenado jura vingança contra Holmes e envia uma mensagem sinistra escondida num pudim natalino.",
        "desc_en": "A condemned murderer plots revenge against Holmes by hiding an explosive warning inside a pudding.",
        "size_mb": 80.3
    },

    # 3. Bonanza (1959-1960)
    {
        "id": "ep_bonanza_s01e20",
        "series_id": "bonanza",
        "title_pt": "Bonanza S01E20 - Os Mercadores do Medo",
        "title_en": "Bonanza S01E20 - The Fear Merchants",
        "year": 1960,
        "group_pt": "Séries | Faroeste Clássico",
        "group_en": "Series | Classic Western",
        "creator": "David Dortort (NBC)",
        "lang": "en",
        "stream_url": "https://archive.org/download/Bonanza-TheFearMerchants/Bonanza_-_The_Fear_Merchants_S01-E20_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_bonanza.svg",
        "desc_pt": "Um candidato a prefeito tenta expulsar trabalhadores chineses de Virginia City, e os Cartwrights tomam posição justa.",
        "desc_en": "A mayoral candidate incites prejudice against Chinese immigrants; the Cartwright family stands for justice.",
        "size_mb": 202.5
    },
    {
        "id": "ep_bonanza_s01e32",
        "series_id": "bonanza",
        "title_pt": "Bonanza S01E32 - Morte ao Amanhecer",
        "title_en": "Bonanza S01E32 - Death at Dawn",
        "year": 1960,
        "group_pt": "Séries | Faroeste Clássico",
        "group_en": "Series | Classic Western",
        "creator": "David Dortort (NBC)",
        "lang": "en",
        "stream_url": "https://archive.org/download/Bonanza-DeathAtDawn/Bonanza_-_Death_At_Dawn_S01-E32_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_bonanza.svg",
        "desc_pt": "Ben Cartwright é feito refém por criminosos que exigem a libertação de um assassino sentenciado à forca.",
        "desc_en": "Ben Cartwright is taken hostage by an outlaw gang demanding the release of a condemned murderer.",
        "size_mb": 206.3
    },
    {
        "id": "ep_bonanza_s02e01",
        "series_id": "bonanza",
        "title_pt": "Bonanza S02E01 - O Confronto Final",
        "title_en": "Bonanza S02E01 - Showdown",
        "year": 1960,
        "group_pt": "Séries | Faroeste Clássico",
        "group_en": "Series | Classic Western",
        "creator": "David Dortort (NBC)",
        "lang": "en",
        "stream_url": "https://archive.org/download/Bonanza-Showdown/Bonanza_-_Showdown_S02-E01_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_bonanza.svg",
        "desc_pt": "Um ex-membro de bando tenta se regenerar trabalhando no rancho Ponderosa, mas seu passado o persegue.",
        "desc_en": "A young outlaw tries to go straight working for the Cartwrights, but his former gang hunts him down.",
        "size_mb": 205.4
    },
    {
        "id": "ep_bonanza_s02e03",
        "series_id": "bonanza",
        "title_pt": "Bonanza S02E03 - Semente de Violência",
        "title_en": "Bonanza S02E03 - Breed of Violence",
        "year": 1960,
        "group_pt": "Séries | Faroeste Clássico",
        "group_en": "Series | Classic Western",
        "creator": "David Dortort (NBC)",
        "lang": "en",
        "stream_url": "https://archive.org/download/Bonanza_-_Breed_Of_Violence/Bonanza_-_Breed_Of_Violence_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_bonanza.svg",
        "desc_pt": "A filha rebelde de um xerife foge com um trapaceiro charmoso; Joe Cartwright parte em seu resgate.",
        "desc_en": "A sheriff's daughter runs away with a charming desperado; Joe Cartwright sets out to save her.",
        "size_mb": 204.6
    },

    # 4. One Step Beyond (1959)
    {
        "id": "ep_one_step_beyond_s01e03",
        "series_id": "one_step_beyond",
        "title_pt": "One Step Beyond S01E03 - O Sonho",
        "title_en": "One Step Beyond S01E03 - The Dream",
        "year": 1959,
        "group_pt": "Séries | Ficção Científica & Sobrenatural",
        "group_en": "Series | Sci-Fi & Supernatural",
        "creator": "Merwin Gerard / John Newland",
        "lang": "en",
        "stream_url": "https://archive.org/download/OneStepBeyondTheDream/OneStepBeyondTheDream.ia.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_one_step_beyond.svg",
        "desc_pt": "Na Segunda Guerra Mundial, um soldado britânico tem visões premonitórias exatas de bombardeios.",
        "desc_en": "During WWII, a British soldier experiences vivid premonitions of an impending air raid.",
        "size_mb": 136.5
    },
    {
        "id": "ep_one_step_beyond_s01e13",
        "series_id": "one_step_beyond",
        "title_pt": "One Step Beyond S01E13 - O Navegador",
        "title_en": "One Step Beyond S01E13 - The Navigator",
        "year": 1959,
        "group_pt": "Séries | Ficção Científica & Sobrenatural",
        "group_en": "Series | Sci-Fi & Supernatural",
        "creator": "Merwin Gerard / John Newland",
        "lang": "en",
        "stream_url": "https://archive.org/download/S1E13THENAVIGATOR/S1E13 - THE NAVIGATOR.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_one_step_beyond.svg",
        "desc_pt": "Um navio à deriva em mar calmo encontra um marinheiro misterioso capaz de guiar a embarcação com precisão impossível.",
        "desc_en": "A drifting vessel is saved by an enigmatic seaman with impossible nautical knowledge.",
        "size_mb": 151.2
    },
    {
        "id": "ep_one_step_beyond_s02e08",
        "series_id": "one_step_beyond",
        "title_pt": "One Step Beyond S02E08 - Mensagem de Clara",
        "title_en": "One Step Beyond S02E08 - Message from Clara",
        "year": 1959,
        "group_pt": "Séries | Ficção Científica & Sobrenatural",
        "group_en": "Series | Sci-Fi & Supernatural",
        "creator": "Merwin Gerard / John Newland",
        "lang": "en",
        "stream_url": "https://archive.org/download/S2E8MESSAGEFROMCLARA/S2E8 - MESSAGE FROM CLARA.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_one_step_beyond.svg",
        "desc_pt": "Uma professora americana escreve em transe palavras em russo que revelam um assassinato iminente.",
        "desc_en": "An American teacher finds herself involuntarily writing in Russian, revealing an urgent warning.",
        "size_mb": 146.2
    },

    # 5. The Lucy Show (1962-1967)
    {
        "id": "ep_the_lucy_show_s01e01",
        "series_id": "the_lucy_show",
        "title_pt": "The Lucy Show S01E01 - Lucy e o Encontro às Cegas",
        "title_en": "The Lucy Show S01E01 - Lucy's Blind Date",
        "year": 1962,
        "group_pt": "Séries | Comédia Clássica",
        "group_en": "Series | Classic Comedy",
        "creator": "Lucille Ball (Desilu / CBS)",
        "lang": "en",
        "stream_url": "https://archive.org/download/lucyshow/lucyshow.ia.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_the_lucy_show.svg",
        "desc_pt": "Lucy e sua amiga Viv organizam um encontro às cegas que rapidamente se transforma em caos e risadas.",
        "desc_en": "Lucy and Viv arrange a blind date that snowballs into trademark Lucille Ball slapstick chaos.",
        "size_mb": 144.0
    },
    {
        "id": "ep_the_lucy_show_s05e21",
        "series_id": "the_lucy_show",
        "title_pt": "The Lucy Show S05E21 - Lucy na Rua Principal",
        "title_en": "The Lucy Show S05E21 - Main Street U.S.A.",
        "year": 1967,
        "group_pt": "Séries | Comédia Clássica",
        "group_en": "Series | Classic Comedy",
        "creator": "Lucille Ball (Desilu / CBS)",
        "lang": "en",
        "stream_url": "https://archive.org/download/Lucy_Show_Main_Street/Lucy_MelTorme.ia.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_the_lucy_show.svg",
        "desc_pt": "Lucy Carmichael luta para impedir a demolição de um quarteirão histórico da sua cidade natal com números musicais.",
        "desc_en": "Lucy fights to preserve historic Main Street with the help of singer Mel Tormé.",
        "size_mb": 143.4
    },

    # 6. As Aventuras de Robin Hood (1955-1956)
    {
        "id": "ep_robin_hood_s01e18",
        "series_id": "robin_hood",
        "title_pt": "As Aventuras de Robin Hood S01E18 - Os Intrusos",
        "title_en": "The Adventures of Robin Hood S01E18 - The Intruders",
        "year": 1955,
        "group_pt": "Séries | Aventura Clássica",
        "group_en": "Series | Classic Adventure",
        "creator": "Hannah Weinstein / Richard Greene",
        "lang": "en",
        "stream_url": "https://archive.org/download/AdventuresOfRobinHoodep18TheIntruders/Adventures of Robin Hood (ep 18 The Intruders).mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_robin_hood.svg",
        "desc_pt": "Robin Hood e seus homens protegem uma aldeia indefesa contra capangas do Xerife de Nottingham.",
        "desc_en": "Robin Hood and Little John defend local villagers from the Sheriff of Nottingham's extortionists.",
        "size_mb": 147.3
    },
    {
        "id": "ep_robin_hood_s01e31",
        "series_id": "robin_hood",
        "title_pt": "As Aventuras de Robin Hood S01E31 - O Tesouro Bizantino",
        "title_en": "The Adventures of Robin Hood S01E31 - Byzantine Treasure",
        "year": 1956,
        "group_pt": "Séries | Aventura Clássica",
        "group_en": "Series | Classic Adventure",
        "creator": "Hannah Weinstein / Richard Greene",
        "lang": "en",
        "stream_url": "https://archive.org/download/AdventuresOfRobinHoodEp31ByzantineTreasureHQ/Adventures of Robin Hood ( ep 31 Byzantine Treasure) HQ.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_robin_hood.svg",
        "desc_pt": "Um emissário com um tesouro precioso busca refúgio na Floresta de Sherwood.",
        "desc_en": "An ambassador carrying imperial treasures seeks protection under Robin Hood's banner.",
        "size_mb": 148.9
    },
    {
        "id": "ep_robin_hood_s01e37",
        "series_id": "robin_hood",
        "title_pt": "As Aventuras de Robin Hood S01E37 - O Cavaleiro para o Jantar",
        "title_en": "The Adventures of Robin Hood S01E37 - The Knight Who Came to Dinner",
        "year": 1956,
        "group_pt": "Séries | Aventura Clássica",
        "group_en": "Series | Classic Adventure",
        "creator": "Hannah Weinstein / Richard Greene",
        "lang": "en",
        "stream_url": "https://archive.org/download/AdventuresOfRobinHoodHQEp37TheKnightWhoCameToDinner/Adventures of Robin Hood HQ ep 37 The Knight Who Came to Dinner.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_robin_hood.svg",
        "desc_pt": "Um nobre falido é recebido pelos foras da lei e descobre a verdadeira honra na floresta.",
        "desc_en": "An impoverished knight encounters Robin Hood and learns the true meaning of honor.",
        "size_mb": 148.6
    },

    # 7. The Dick Van Dyke Show (1962)
    {
        "id": "ep_dick_van_dyke_s02e01",
        "series_id": "dick_van_dyke",
        "title_pt": "The Dick Van Dyke Show S02E01 - Nunca Dê Nome a um Pato",
        "title_en": "The Dick Van Dyke Show S02E01 - Never Name a Duck",
        "year": 1962,
        "group_pt": "Séries | Comédia Clássica",
        "group_en": "Series | Classic Comedy",
        "creator": "Carl Reiner",
        "lang": "en",
        "stream_url": "https://archive.org/download/dick_van_dyke_show_31_never_name_a_duck/dick_van_dyke_show_31_never_name_a_duck_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_dick_van_dyke.svg",
        "desc_pt": "Rob e Laura Petrie tentam cuidar de patinhos de estimação em casa, desatando confusões familiares hilárias.",
        "desc_en": "Rob brings home baby ducks for his son Ritchie, leading to suburban comic turmoil.",
        "size_mb": 104.0
    },
    {
        "id": "ep_dick_van_dyke_s02e04",
        "series_id": "dick_van_dyke",
        "title_pt": "The Dick Van Dyke Show S02E04 - A Caderneta de Poupança",
        "title_en": "The Dick Van Dyke Show S02E04 - Bank Book 6565696",
        "year": 1962,
        "group_pt": "Séries | Comédia Clássica",
        "group_en": "Series | Classic Comedy",
        "creator": "Carl Reiner",
        "lang": "en",
        "stream_url": "https://archive.org/download/dick_van_dyke_show_34_bank_book_6565696/dick_van_dyke_show_34_bank_book_6565696_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_dick_van_dyke.svg",
        "desc_pt": "Rob encontra uma conta bancária secreta de Laura e começa a suspeitar de gastos misteriosos.",
        "desc_en": "Rob finds a secret passbook and suspects Laura of hiding a fortune.",
        "size_mb": 106.3
    },
    {
        "id": "ep_dick_van_dyke_s02e09",
        "series_id": "dick_van_dyke",
        "title_pt": "The Dick Van Dyke Show S02E09 - A Noite em que o Teto Caiu",
        "title_en": "The Dick Van Dyke Show S02E09 - The Night the Roof Fell In",
        "year": 1962,
        "group_pt": "Séries | Comédia Clássica",
        "group_en": "Series | Classic Comedy",
        "creator": "Carl Reiner",
        "lang": "en",
        "stream_url": "https://archive.org/download/dick_van_dyke_show_39_the_night_the_roof_fell_in/dick_van_dyke_show_39_the_night_the_roof_fell_in_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_dick_van_dyke.svg",
        "desc_pt": "Um dia frustrante no trabalho e em casa contado através de três perspectivas cômicas diferentes (Rob, Laura e o peixinho).",
        "desc_en": "A marital squabble told through three contrasting and hilarious points of view.",
        "size_mb": 105.4
    },

    # 8. Dragnet (1952-1953)
    {
        "id": "ep_dragnet_s01e05",
        "series_id": "dragnet",
        "title_pt": "Dragnet S01E05 - The Big Cast",
        "title_en": "Dragnet S01E05 - The Big Cast",
        "year": 1952,
        "group_pt": "Séries | Mistério & Policial",
        "group_en": "Series | Mystery & Crime",
        "creator": "Jack Webb",
        "lang": "en",
        "stream_url": "https://archive.org/download/DragnetS01E05TheBigCast/Dragnet S01E05 The Big Cast - Watch Crime Series Online.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_dragnet.svg",
        "desc_pt": "O Sargento Joe Friday interroga um homem suspeito que confessa assassinatos múltiplos em Los Angeles.",
        "desc_en": "Sgt. Joe Friday and Frank Smith interrogate a man who casually confesses to multiple homicides.",
        "size_mb": 72.1
    },
    {
        "id": "ep_dragnet_s02e15",
        "series_id": "dragnet",
        "title_pt": "Dragnet S02E15 - The Big Betty",
        "title_en": "Dragnet S02E15 - The Big Betty",
        "year": 1953,
        "group_pt": "Séries | Mistério & Policial",
        "group_en": "Series | Mystery & Crime",
        "creator": "Jack Webb",
        "lang": "en",
        "stream_url": "https://archive.org/download/DragnetTheBigBetty/Dragnet - The Big Bar.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_dragnet.svg",
        "desc_pt": "Friday e Smith desmantelam um esquema fraudulento que engana famílias de luto vendendo joias e bíblias falsas.",
        "desc_en": "Friday targets heartless con artists preying on grieving widows in post-war Los Angeles.",
        "size_mb": 69.7
    },

    # 9. Flash Gordon (1954-1955)
    {
        "id": "ep_flash_gordon_s01e05",
        "series_id": "flash_gordon",
        "title_pt": "Flash Gordon S01E05 - Akim, o Terrível",
        "title_en": "Flash Gordon S01E05 - Akim the Terrible",
        "year": 1954,
        "group_pt": "Séries | Ficção Científica & Aventura",
        "group_en": "Series | Sci-Fi & Adventure",
        "creator": "Steve Holland / Universal",
        "lang": "en",
        "stream_url": "https://archive.org/download/FlashGordon-AkimTheTerrible-1954-Ep1x05/FlashGordon105-AkimTheTerrible_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_flash_gordon.svg",
        "desc_pt": "Flash Gordon, Dale Arden e Dr. Zarkov enfrentam um déspota cruel que planeja escravizar planetas vizinhos.",
        "desc_en": "Flash Gordon and his crew journey to thwart the despotic schemes of cosmic villain Akim.",
        "size_mb": 104.9
    },
    {
        "id": "ep_flash_gordon_s01e19",
        "series_id": "flash_gordon",
        "title_pt": "Flash Gordon S01E19 - Corrida Contra o Tempo",
        "title_en": "Flash Gordon S01E19 - The Race Against Time",
        "year": 1955,
        "group_pt": "Séries | Ficção Científica & Aventura",
        "group_en": "Series | Sci-Fi & Adventure",
        "creator": "Steve Holland / Universal",
        "lang": "en",
        "stream_url": "https://archive.org/download/FlashGordon-TheRaceAgainstTime-1955/FlashGordon119-TheRaceAgainstTime_512kb.mp4",
        "logo_url": "https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/poster_flash_gordon.svg",
        "desc_pt": "Uma substância cósmica rara é necessária com urgência para salvar uma civilização inteira de catástrofe.",
        "desc_en": "Flash Gordon embarks on a desperate high-speed space mission to secure a cure for an ailing world.",
        "size_mb": 109.6
    }
]

# Creative Commons Open Movies
OPEN_MOVIES_DATA = [
    {
        "id": "BigBuckBunny_2008",
        "title_pt": "Big Buck Bunny",
        "title_en": "Big Buck Bunny",
        "year": 2008,
        "director": "Sacha Goedegebure (Blender Foundation)",
        "lang": "Universal",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/512px-Big_buck_bunny_poster_big.jpg",
        "url": "https://archive.org/download/BigBuckBunny_124/Content/big_buck_bunny_720p_surround.mp4",
        "desc_pt": "Clássico curta-metragem aberto da Blender Foundation sobre um coelho gigante e esquilos travessos. Licença CC-BY 3.0.",
        "desc_en": "Blender Foundation's landmark open comedy film about a giant rabbit and bullying forest creatures. CC-BY 3.0."
    },
    {
        "id": "Sintel_2010",
        "title_pt": "Sintel (A Busca do Dragão)",
        "title_en": "Sintel (The Dragon Girl)",
        "year": 2010,
        "director": "Colin Levy (Blender Foundation)",
        "lang": "en",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Sintel_poster.jpg/512px-Sintel_poster.jpg",
        "url": "https://archive.org/download/Sintel/sintel-2048-surround.mp4",
        "desc_pt": "Emocionante curta épico de fantasia sobre uma jovem guerreira que resgata um pequeno dragão. Licença CC-BY 3.0.",
        "desc_en": "Epic fantasy open animated movie about a lonely girl who rescues and bonds with a baby dragon. CC-BY 3.0."
    },
    {
        "id": "TearsOfSteel_2012",
        "title_pt": "Tears of Steel (Lágrimas de Aço)",
        "title_en": "Tears of Steel",
        "year": 2012,
        "director": "Ian Hubert (Blender Foundation)",
        "lang": "en",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Tears_of_Steel_poster.jpg/512px-Tears_of_Steel_poster.jpg",
        "url": "https://archive.org/download/Tears-of-Steel/tears_of_steel_1080p.mp4",
        "desc_pt": "Ficção científica pós-apocalíptica em Amsterdã combinando atores reais e CGI aberto. Licença CC-BY 3.0.",
        "desc_en": "Post-apocalyptic science fiction short combining live-action actors with open CGI visual effects. CC-BY 3.0."
    },
    {
        "id": "ElephantsDream_2006",
        "title_pt": "Elephants Dream (O Sonho dos Elefantes)",
        "title_en": "Elephants Dream",
        "year": 2006,
        "director": "Bassam Kurdali (Blender Foundation)",
        "lang": "en",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Elephants_Dream_poster.jpg/512px-Elephants_Dream_poster.jpg",
        "url": "https://archive.org/download/ElephantsDream/ed_1024.mp4",
        "desc_pt": "O primeiro filme de animação 3D totalmente aberto da história do cinema digital. Licença CC-BY 2.5.",
        "desc_en": "The world's first open-source 3D CGI animated short film. CC-BY 2.5."
    },
    {
        "id": "CosmosLaundromat_2015",
        "title_pt": "Cosmos Laundromat (Lavanderia Cósmica)",
        "title_en": "Cosmos Laundromat",
        "year": 2015,
        "director": "Mathieu Auvray (Blender Foundation)",
        "lang": "en",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Cosmos_Laundromat_-_Poster.png/512px-Cosmos_Laundromat_-_Poster.png",
        "url": "https://archive.org/download/CosmosLaundromatFirstCycle/Cosmos%20Laundromat%20-%20First%20Cycle%20%281080p%29.mp4",
        "desc_pt": "Em uma ilha desolada, uma ovelha suicida recebe uma oferta para vivenciar infinitas vidas alternativas. Licença CC-BY.",
        "desc_en": "On a desolate island, a suicidal sheep meets a mysterious salesman offering infinite alternative lives. CC-BY."
    }
]

def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    primary_path = os.path.join(root_dir, 'data', 'resolved_archive_items.json')
    extra_path = os.path.join(root_dir, 'data', 'extra_resolved.json')
    anim_path = os.path.join(root_dir, 'data', 'verified_animations_all.json')
    
    with open(primary_path, 'r', encoding='utf-8') as f:
        primary = json.load(f)
    with open(extra_path, 'r', encoding='utf-8') as f:
        extra = json.load(f)
    with open(anim_path, 'r', encoding='utf-8') as f:
        animations = json.load(f)
        
    return primary, extra, animations

def build_bilingual_catalogs():
    primary, extra, animations = load_data()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    catalog_dir = os.path.join(root_dir, 'catalog')
    pt_dir = os.path.join(catalog_dir, 'pt')
    en_dir = os.path.join(catalog_dir, 'en')
    
    os.makedirs(pt_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)

    # Categories Mapping (PT and EN)
    genre_meta = {
        'Terror / Horror': ('Filmes | Terror, Sci-Fi & Cult Clássico', 'Movies | Classic Horror, Sci-Fi & Cult'),
        'Terror / Comédia': ('Filmes | Terror, Sci-Fi & Cult Clássico', 'Movies | Classic Horror, Sci-Fi & Cult'),
        'Ficção Científica / Cult': ('Filmes | Terror, Sci-Fi & Cult Clássico', 'Movies | Classic Horror, Sci-Fi & Cult'),
        'Ficção Científica / Horror': ('Filmes | Terror, Sci-Fi & Cult Clássico', 'Movies | Classic Horror, Sci-Fi & Cult'),
        'Ficção Científica / Obra-Prima': ('Filmes | Terror, Sci-Fi & Cult Clássico', 'Movies | Classic Horror, Sci-Fi & Cult'),
        'Mistério / Romance': ('Filmes | Clássicos do Cinema Mundial (Drama & Romance)', 'Movies | World Cinema Classics (Drama & Romance)'),
        'Comédia Romântica': ('Filmes | Clássicos do Cinema Mundial (Drama & Romance)', 'Movies | World Cinema Classics (Drama & Romance)'),
        'Drama / Musical': ('Filmes | Clássicos do Cinema Mundial (Drama & Romance)', 'Movies | World Cinema Classics (Drama & Romance)'),
        'Suspense / Noir': ('Filmes | Film Noir, Policial & Mistério', 'Movies | Film Noir & Mystery'),
        'Film Noir': ('Filmes | Film Noir, Policial & Mistério', 'Movies | Film Noir & Mystery'),
        'Mistério / Policial': ('Filmes | Film Noir, Policial & Mistério', 'Movies | Film Noir & Mystery'),
        'Comédia / Ação / Mudo': ('Filmes | Comédia & Cinema Mudo', 'Movies | Comedy & Silent Cinema'),
        'Comédia / Mudo': ('Filmes | Comédia & Cinema Mudo', 'Movies | Comedy & Silent Cinema'),
        'Comédia': ('Filmes | Comédia & Cinema Mudo', 'Movies | Comedy & Silent Cinema'),
        'Western': ('Filmes | Faroeste & Western', 'Movies | Classic Westerns'),
        'Cinema Brasileiro / Vanguarda': ('Filmes | Patrimônio do Cinema Brasileiro', 'Movies | Brazilian Cinema Heritage'),
        'Cinema Brasileiro / Clássico': ('Filmes | Patrimônio do Cinema Brasileiro', 'Movies | Brazilian Cinema Heritage'),
        'Cinema Brasileiro / Histórico': ('Filmes | Patrimônio do Cinema Brasileiro', 'Movies | Brazilian Cinema Heritage'),
        'Cinema Brasileiro / Documentário': ('Filmes | Patrimônio do Cinema Brasileiro', 'Movies | Brazilian Cinema Heritage'),
        'Arquivo Histórico / Cinejornal': ('Filmes | Arquivos Históricos & Cinejornais', 'Movies | Historical Archives & Vintage Newsreels'),
        'Arquivo Histórico / Esporte': ('Filmes | Arquivos Históricos & Cinejornais', 'Movies | Historical Archives & Vintage Newsreels'),
        'Documentário / Guerra Fria': ('Filmes | Arquivos Históricos & Cinejornais', 'Movies | Historical Archives & Vintage Newsreels'),
        'Documentário / Futurismo 50s': ('Filmes | Arquivos Históricos & Cinejornais', 'Movies | Historical Archives & Vintage Newsreels')
    }

    # Bilingual metadata for Extra Resolved Movies
    extra_movies_meta = {
        'The Last Man on Earth': {
            'title_pt': 'The Last Man on Earth (Mortos Que Matam)',
            'title_en': 'The Last Man on Earth',
            'year': 1964,
            'group_pt': 'Filmes | Terror, Sci-Fi & Cult Clássico',
            'group_en': 'Movies | Classic Horror, Sci-Fi & Cult',
            'director': 'Vincent Price',
            'lang': 'en',
            'desc_pt': 'Primeira adaptação do romance Eu Sou a Lenda de Richard Matheson.',
            'desc_en': 'First film adaptation of Richard Matheson\'s I Am Legend starring Vincent Price.'
        },
        'White Zombie': {
            'title_pt': 'White Zombie (Zumbi Branco)',
            'title_en': 'White Zombie',
            'year': 1932,
            'group_pt': 'Filmes | Terror, Sci-Fi & Cult Clássico',
            'group_en': 'Movies | Classic Horror, Sci-Fi & Cult',
            'director': 'Bela Lugosi',
            'lang': 'en',
            'desc_pt': 'O primeiro longa-metragem sobre mortos-vivos da história do cinema.',
            'desc_en': 'The first feature-length zombie film in cinema history, starring Bela Lugosi.'
        },
        'Meet John Doe': {
            'title_pt': 'Meet John Doe (Adorável Vagabundo)',
            'title_en': 'Meet John Doe',
            'year': 1941,
            'group_pt': 'Filmes | Clássicos do Cinema Mundial (Drama & Romance)',
            'group_en': 'Movies | World Cinema Classics (Drama & Romance)',
            'director': 'Frank Capra, Gary Cooper, Barbara Stanwyck',
            'lang': 'en',
            'desc_pt': 'Magistral obra de Frank Capra sobre o poder da mídia e a dignidade humana.',
            'desc_en': 'Frank Capra\'s classic drama about journalism, politics, and the common man.'
        },
        'My Man Godfrey': {
            'title_pt': 'My Man Godfrey (Irene, a Teimosa)',
            'title_en': 'My Man Godfrey',
            'year': 1936,
            'group_pt': 'Filmes | Clássicos do Cinema Mundial (Drama & Romance)',
            'group_en': 'Movies | World Cinema Classics (Drama & Romance)',
            'director': 'William Powell, Carole Lombard',
            'lang': 'en',
            'desc_pt': 'Hilariante clássico screwball comedy dos anos 1930.',
            'desc_en': 'Definitive screwball comedy classic starring William Powell and Carole Lombard.'
        },
        'The Snows of Kilimanjaro': {
            'title_pt': 'The Snows of Kilimanjaro (As Neves do Kilimanjaro)',
            'title_en': 'The Snows of Kilimanjaro',
            'year': 1952,
            'group_pt': 'Filmes | Clássicos do Cinema Mundial (Drama & Romance)',
            'group_en': 'Movies | World Cinema Classics (Drama & Romance)',
            'director': 'Gregory Peck, Susan Hayward, Ava Gardner',
            'lang': 'en',
            'desc_pt': 'Baseado no conto de Ernest Hemingway em luxuoso Technicolor.',
            'desc_en': 'Hemingway adaptation in lavish Technicolor starring Gregory Peck and Ava Gardner.'
        },
        'Steamboat Bill, Jr.': {
            'title_pt': 'Steamboat Bill, Jr. (Marinheiro de Encomenda)',
            'title_en': 'Steamboat Bill, Jr.',
            'year': 1928,
            'group_pt': 'Filmes | Comédia & Cinema Mudo',
            'group_en': 'Movies | Comedy & Silent Cinema',
            'director': 'Buster Keaton',
            'lang': 'silent',
            'desc_pt': 'Buster Keaton e a lendária cena do ciclone sem dublês.',
            'desc_en': 'Buster Keaton comedy masterpiece featuring the famous cyclone house-facade stunt.'
        },
        'Sherlock Jr.': {
            'title_pt': 'Sherlock Jr. (Buster Keaton)',
            'title_en': 'Sherlock Jr.',
            'year': 1924,
            'group_pt': 'Filmes | Comédia & Cinema Mudo',
            'group_en': 'Movies | Comedy & Silent Cinema',
            'director': 'Buster Keaton',
            'lang': 'silent',
            'desc_pt': 'Projecionista entra dentro do filme dos seus sonhos para desvendar crime.',
            'desc_en': 'A projectionist dreams he enters the movie screen to become a master detective.'
        },
        'The Kid': {
            'title_pt': 'The Kid (O Garoto)',
            'title_en': 'The Kid',
            'year': 1921,
            'group_pt': 'Filmes | Comédia & Cinema Mudo',
            'group_en': 'Movies | Comedy & Silent Cinema',
            'director': 'Charlie Chaplin, Jackie Coogan',
            'lang': 'silent',
            'desc_pt': 'O primeiro longa-metragem dirigido por Chaplin, mesclando humor genial e emoção.',
            'desc_en': 'Chaplin\'s first feature film, masterpiece of comedy and pathos with Jackie Coogan.'
        },
        'The Gold Rush': {
            'title_pt': 'The Gold Rush (Em Busca do Ouro)',
            'title_en': 'The Gold Rush',
            'year': 1925,
            'group_pt': 'Filmes | Comédia & Cinema Mudo',
            'group_en': 'Movies | Comedy & Silent Cinema',
            'director': 'Charlie Chaplin',
            'lang': 'silent',
            'desc_pt': 'A icônica dança dos pãezinhos e o banquete da bota na corrida do ouro.',
            'desc_en': 'The Little Tramp in the Klondike gold rush featuring the classic bread roll dance.'
        },
        'The Vagabond': {
            'title_pt': 'The Vagabond (O Vagabundo)',
            'title_en': 'The Vagabond',
            'year': 1916,
            'group_pt': 'Filmes | Comédia & Cinema Mudo',
            'group_en': 'Movies | Comedy & Silent Cinema',
            'director': 'Charlie Chaplin, Edna Purviance',
            'lang': 'silent',
            'desc_pt': 'Clássico curta mudo de Chaplin com violino e romance cigano.',
            'desc_en': 'Early Chaplin silent comedy short with gypsy romance and violin melodies.'
        },
        'Safety Last!': {
            'title_pt': 'Safety Last! (O Homem Mosca)',
            'title_en': 'Safety Last!',
            'year': 1923,
            'group_pt': 'Filmes | Comédia & Cinema Mudo',
            'group_en': 'Movies | Comedy & Silent Cinema',
            'director': 'Harold Lloyd',
            'lang': 'silent',
            'desc_pt': 'A célebre cena de Harold Lloyd pendurado nos ponteiros do relógio do edifício.',
            'desc_en': 'Iconic silent comedy image of Harold Lloyd dangling from skyscraper clock hands.'
        },
        'D.O.A.': {
            'title_pt': 'D.O.A. (Com as Horas Contadas)',
            'title_en': 'D.O.A.',
            'year': 1950,
            'group_pt': 'Filmes | Film Noir, Policial & Mistério',
            'group_en': 'Movies | Film Noir & Mystery',
            'director': 'Rudolph Maté, Edmond O\'Brien',
            'lang': 'en',
            'desc_pt': 'Homem envenenado corre contra o relógio para desvendar seu próprio assassinato.',
            'desc_en': 'A poisoned accountant races against the clock to solve his own impending murder.'
        },
        'Scarlet Street': {
            'title_pt': 'Scarlet Street (Almas Perversas)',
            'title_en': 'Scarlet Street',
            'year': 1945,
            'group_pt': 'Filmes | Film Noir, Policial & Mistério',
            'group_en': 'Movies | Film Noir & Mystery',
            'director': 'Fritz Lang, Edward G. Robinson',
            'lang': 'en',
            'desc_pt': 'Direção precisa de Fritz Lang sobre engano, traição e tragédia moral.',
            'desc_en': 'Fritz Lang\'s acclaimed noir thriller about obsession, deception, and moral downfall.'
        },
        'Detour': {
            'title_pt': 'Detour (Curva do Destino)',
            'title_en': 'Detour',
            'year': 1945,
            'group_pt': 'Filmes | Film Noir, Policial & Mistério',
            'group_en': 'Movies | Film Noir & Mystery',
            'director': 'Edgar G. Ulmer',
            'lang': 'en',
            'desc_pt': 'O mais famoso e influente filme B noir da história do cinema.',
            'desc_en': 'The quintessential B-movie film noir masterpiece directed by Edgar G. Ulmer.'
        },
        'Sherlock Holmes: The Woman in Green': {
            'title_pt': 'Sherlock Holmes: The Woman in Green (A Mulher de Verde)',
            'title_en': 'Sherlock Holmes: The Woman in Green',
            'year': 1945,
            'group_pt': 'Filmes | Film Noir, Policial & Mistério',
            'group_en': 'Movies | Film Noir & Mystery',
            'director': 'Basil Rathbone, Nigel Bruce',
            'lang': 'en',
            'desc_pt': 'Holmes investiga uma série de assassinatos misteriosos orquestrados pelo Professor Moriarty.',
            'desc_en': 'Sherlock Holmes and Dr. Watson confront Professor Moriarty in London.'
        },
        'Sherlock Holmes: Secret Weapon': {
            'title_pt': 'Sherlock Holmes and the Secret Weapon (A Arma Secreta)',
            'title_en': 'Sherlock Holmes and the Secret Weapon',
            'year': 1942,
            'group_pt': 'Filmes | Film Noir, Policial & Mistério',
            'group_en': 'Movies | Film Noir & Mystery',
            'director': 'Basil Rathbone, Nigel Bruce',
            'lang': 'en',
            'desc_pt': 'Holmes e Watson em perigosa missão contra agentes inimigos na 2ª Guerra.',
            'desc_en': 'Holmes protects a scientist and secret bombsight from wartime espionage.'
        },
        'Angel and the Badman': {
            'title_pt': 'Angel and the Badman (O Anjo e o Bandido)',
            'title_en': 'Angel and the Badman',
            'year': 1947,
            'group_pt': 'Filmes | Faroeste & Western',
            'group_en': 'Movies | Classic Westerns',
            'director': 'John Wayne, Gail Russell',
            'lang': 'en',
            'desc_pt': 'Pistoleiro foragido acolhido por família pacifista reavalia suas escolhas.',
            'desc_en': 'John Wayne stars as an injured outlaw taken in by a peaceful Quaker family.'
        },
        'Trip to the Moon': {
            'title_pt': 'A Trip to the Moon (Viagem à Lua)',
            'title_en': 'A Trip to the Moon (Le Voyage dans la Lune)',
            'year': 1902,
            'group_pt': 'Filmes | Arquivos Históricos & Cinejornais',
            'group_en': 'Movies | Historical Archives & Vintage Newsreels',
            'director': 'Georges Méliès',
            'lang': 'silent',
            'desc_pt': 'O primeiro clássico de ficção científica da história do cinema mundial.',
            'desc_en': 'Georges Méliès landmark 1902 film, the very first science fiction movie in history.'
        }
    }

    # Lists for PT and EN catalogs
    catalog_pt = []
    catalog_en = []

    # 1. Channels organized by Country
    for ch in LIVE_CHANNELS_DATA:
        # Group by Country
        group_pt = f"Canais ao Vivo - {ch['country_pt']}"
        group_en = f"Live Channels - {ch['country_en']}"
        
        # Link logo to GitHub repository raw URL
        ref_filename = os.path.basename(ch["ref_logo"])
        raw_logo_url = f"https://raw.githubusercontent.com/bitinfinitus/public-domain-catalog/refs/heads/main/logos/{ref_filename}"
        
        item_pt = {
            "id": ch["id"],
            "title": ch["name_pt"],
            "year": None,
            "group": group_pt,
            "country": ch["country"],
            "lang": ch["lang"],
            "stream_url": ch["url"],
            "logo_url": raw_logo_url,
            "ref_logo": ch["ref_logo"],
            "external_logo": ch["logo"],
            "desc": ch["desc_pt"],
            "type": "live_stream"
        }
        item_en = {
            "id": ch["id"],
            "title": ch["name_en"],
            "year": None,
            "group": group_en,
            "country": ch["country"],
            "lang": ch["lang"],
            "stream_url": ch["url"],
            "logo_url": raw_logo_url,
            "ref_logo": ch["ref_logo"],
            "external_logo": ch["logo"],
            "desc": ch["desc_en"],
            "type": "live_stream"
        }
        catalog_pt.append(item_pt)
        catalog_en.append(item_en)

    # 2. Cinema & Heritage Items (Primary)
    for it in primary:
        genre = it.get('genre', '')
        if 'Animação' in genre:
            continue
        g_pt, g_en = genre_meta.get(genre, ('Filmes | Clássicos do Cinema Mundial (Drama & Romance)', 'Movies | World Cinema Classics (Drama & Romance)'))
        title_raw = it.get('title', '')
        
        catalog_pt.append({
            "id": it.get('identifier'),
            "title": title_raw,
            "year": it.get('year'),
            "group": g_pt,
            "director": it.get('director'),
            "lang": it.get('lang'),
            "stream_url": it.get('stream_url'),
            "logo_url": it.get('logo_url'),
            "desc": it.get('synopsis', ''),
            "size_mb": it.get('size_mb'),
            "type": "vod_archive"
        })
        # Strip Portuguese alternate titles from English title if present
        clean_en_title = title_raw.split(' (')[0] if ' (' in title_raw and any(k in title_raw for k in ['Jejum', 'Nasce', 'Estranho', 'General', 'Garoto', 'Ouro', 'Imigrante', 'Vagabundo', 'Tolos']) else title_raw
        catalog_en.append({
            "id": it.get('identifier'),
            "title": clean_en_title,
            "year": it.get('year'),
            "group": g_en,
            "director": it.get('director'),
            "lang": it.get('lang'),
            "stream_url": it.get('stream_url'),
            "logo_url": it.get('logo_url'),
            "desc": it.get('synopsis', ''),
            "size_mb": it.get('size_mb'),
            "type": "vod_archive"
        })

    # 3. Cinema & Heritage Items (Extra)
    for it in extra:
        name = it.get('name')
        if name not in extra_movies_meta:
            continue
        m = extra_movies_meta[name]
        catalog_pt.append({
            "id": it.get('identifier'),
            "title": m['title_pt'],
            "year": m['year'],
            "group": m['group_pt'],
            "director": m['director'],
            "lang": m['lang'],
            "stream_url": it.get('stream_url'),
            "logo_url": it.get('logo_url'),
            "desc": m['desc_pt'],
            "size_mb": it.get('size_mb'),
            "type": "vod_archive"
        })
        catalog_en.append({
            "id": it.get('identifier'),
            "title": m['title_en'],
            "year": m['year'],
            "group": m['group_en'],
            "director": m['director'],
            "lang": m['lang'],
            "stream_url": it.get('stream_url'),
            "logo_url": it.get('logo_url'),
            "desc": m['desc_en'],
            "size_mb": it.get('size_mb'),
            "type": "vod_archive"
        })

    # 4. Complete Animations (46 titles)
    for anim in animations:
        catalog_pt.append({
            "id": anim["id"],
            "title": anim["title"],
            "year": anim.get("year"),
            "group": "Filmes | Animações Clássicas de Domínio Público",
            "director": anim.get("director") or anim.get("studio"),
            "lang": anim.get("lang", "en"),
            "stream_url": anim["stream_url"],
            "logo_url": anim["logo_url"],
            "desc": anim.get("desc", ""),
            "size_mb": anim.get("size_mb"),
            "type": "vod_animation"
        })
        catalog_en.append({
            "id": anim["id"],
            "title": anim["title"],
            "year": anim.get("year"),
            "group": "Movies | Classic Public Domain Animation",
            "director": anim.get("director") or anim.get("studio"),
            "lang": anim.get("lang", "en"),
            "stream_url": anim["stream_url"],
            "logo_url": anim["logo_url"],
            "desc": anim.get("desc", ""),
            "size_mb": anim.get("size_mb"),
            "type": "vod_animation"
        })

    # 5. Open Movies (5)
    for om in OPEN_MOVIES_DATA:
        catalog_pt.append({
            "id": om["id"],
            "title": om["title_pt"],
            "year": om["year"],
            "group": "Filmes | Cinema Aberto & Creative Commons",
            "director": om["director"],
            "lang": om["lang"],
            "stream_url": om["url"],
            "logo_url": om["logo"],
            "desc": om["desc_pt"],
            "type": "vod_open_cinema"
        })
        catalog_en.append({
            "id": om["id"],
            "title": om["title_en"],
            "year": om["year"],
            "group": "Movies | Open Cinema & Creative Commons",
            "director": om["director"],
            "lang": om["lang"],
            "stream_url": om["url"],
            "logo_url": om["logo"],
            "desc": om["desc_en"],
            "type": "vod_open_cinema"
        })

    # 6. Classic TV Series (26 episodes across 9 iconic series, SxxExx formatted)
    for s in SERIES_DATA:
        catalog_pt.append({
            "id": s["id"],
            "title": s["title_pt"],
            "year": s["year"],
            "group": s["group_pt"],
            "director": s["creator"],
            "lang": s["lang"],
            "stream_url": s["stream_url"],
            "logo_url": s["logo_url"],
            "desc": s["desc_pt"],
            "size_mb": s.get("size_mb"),
            "type": "vod_series"
        })
        catalog_en.append({
            "id": s["id"],
            "title": s["title_en"],
            "year": s["year"],
            "group": s["group_en"],
            "director": s["creator"],
            "lang": s["lang"],
            "stream_url": s["stream_url"],
            "logo_url": s["logo_url"],
            "desc": s["desc_en"],
            "size_mb": s.get("size_mb"),
            "type": "vod_series"
        })

    # Save JSON Databases
    with open(os.path.join(catalog_dir, 'catalog_pt.json'), 'w', encoding='utf-8') as f:
        json.dump(catalog_pt, f, ensure_ascii=False, indent=2)
    with open(os.path.join(catalog_dir, 'catalog_en.json'), 'w', encoding='utf-8') as f:
        json.dump(catalog_en, f, ensure_ascii=False, indent=2)
    with open(os.path.join(catalog_dir, 'catalog.json'), 'w', encoding='utf-8') as f:
        json.dump(catalog_pt, f, ensure_ascii=False, indent=2)

    # 6. Generate Master Playlists (PT and EN)
    master_pt_path = os.path.join(pt_dir, 'public_domain_master_pt.m3u8')
    generate_m3u8(catalog_pt, master_pt_path, 'Catálogo Oficial de Domínio Público (Master PT)')

    master_en_path = os.path.join(en_dir, 'public_domain_master_en.m3u8')
    generate_m3u8(catalog_en, master_en_path, 'Official Public Domain Catalog (Master EN)')

    # Compatibility Root Master Playlist
    root_master_path = os.path.join(catalog_dir, 'public_domain_master.m3u8')
    generate_m3u8(catalog_pt, root_master_path, 'Catálogo Oficial de Domínio Público (Master)')

    # Consolidated Tier Playlists (Series, Movies, Live Channels)
    # 1. Complete Series Playlists
    series_pt = [m for m in catalog_pt if m['type'] == 'vod_series']
    generate_m3u8(series_pt, os.path.join(pt_dir, 'series_classicas_de_tv_dominio_publico.m3u8'), 'Séries Clássicas de TV em Domínio Público')
    series_en = [m for m in catalog_en if m['type'] == 'vod_series']
    generate_m3u8(series_en, os.path.join(en_dir, 'classic_tv_series_public_domain.m3u8'), 'Classic TV Series in the Public Domain')

    # 2. Complete Movies Playlists
    movies_pt = [m for m in catalog_pt if m['type'] in ['vod_archive', 'vod_animation', 'vod_open_cinema']]
    generate_m3u8(movies_pt, os.path.join(pt_dir, 'filmes_cinema_e_animacoes.m3u8'), 'Filmes e Animações em Domínio Público')
    movies_en = [m for m in catalog_en if m['type'] in ['vod_archive', 'vod_animation', 'vod_open_cinema']]
    generate_m3u8(movies_en, os.path.join(en_dir, 'movies_cinema_and_animation.m3u8'), 'Movies and Classic Animation in the Public Domain')

    # 3. Complete Live Channels Playlists
    live_pt = [m for m in catalog_pt if m['type'] == 'live_stream']
    generate_m3u8(live_pt, os.path.join(pt_dir, 'canais_ao_vivo_todos.m3u8'), 'Canais Públicos e Educativos ao Vivo')
    live_en = [m for m in catalog_en if m['type'] == 'live_stream']
    generate_m3u8(live_en, os.path.join(en_dir, 'live_channels_all.m3u8'), 'Live Public and Educational Channels')

    # 7. Generate Segmented Playlists for PT
    pt_groups = sorted(list(set(m['group'] for m in catalog_pt)))
    for g in pt_groups:
        items = [m for m in catalog_pt if m['group'] == g]
        # Clean slug
        slug = (g.lower()
                .replace(' ', '_')
                .replace('|', '')
                .replace('__', '_')
                .replace('&', 'e')
                .replace(',', '')
                .replace('(', '')
                .replace(')', '')
                .replace('á', 'a')
                .replace('ã', 'a')
                .replace('â', 'a')
                .replace('é', 'e')
                .replace('ê', 'e')
                .replace('í', 'i')
                .replace('ó', 'o')
                .replace('ô', 'o')
                .replace('õ', 'o')
                .replace('ú', 'u')
                .replace('ç', 'c')
                .strip('_'))
        filepath = os.path.join(pt_dir, f"{slug}.m3u8")
        generate_m3u8(items, filepath, f"Domínio Público - {g}")

    # 8. Generate Segmented Playlists for EN
    en_groups = sorted(list(set(m['group'] for m in catalog_en)))
    for g in en_groups:
        items = [m for m in catalog_en if m['group'] == g]
        slug = (g.lower()
                .replace(' ', '_')
                .replace('|', '')
                .replace('__', '_')
                .replace('&', 'and')
                .replace(',', '')
                .replace('(', '')
                .replace(')', '')
                .strip('_'))
        filepath = os.path.join(en_dir, f"{slug}.m3u8")
        generate_m3u8(items, filepath, f"Public Domain - {g}")

    print(f"\n==========================================")
    print(f"Bilingual Catalog Build Complete!")
    print(f"Total Entries: {len(catalog_pt)} (PT) / {len(catalog_en)} (EN)")
    print(f"PT Groups ({len(pt_groups)}):")
    for g in pt_groups:
        cnt = len([m for m in catalog_pt if m['group'] == g])
        print(f"  - {g}: {cnt} itens")
    print(f"EN Groups ({len(en_groups)}):")
    for g in en_groups:
        cnt = len([m for m in catalog_en if m['group'] == g])
        print(f"  - {g}: {cnt} items")
    print(f"==========================================")

def generate_m3u8(items, filepath, playlist_title):
    lines = [
        "#EXTM3U",
        f"#PLAYLIST:{playlist_title}",
        "#EXT-X-VERSION:3",
        ""
    ]
    for item in items:
        tvg_id = item.get('id', '')
        title = item.get('title', '')
        is_series = item.get('type') == 'vod_series'
        year_str = f" ({item.get('year')})" if (item.get('year') and not is_series) else ""
        full_display_title = f"{title}{year_str}"
        group = item.get('group', 'Domínio Público')
        logo = item.get('logo_url', '')
        stream_url = item.get('stream_url', '')
        lang = item.get('lang', '')
        country = item.get('country', '')
        
        extinf_parts = [
            f'#EXTINF:-1 tvg-id="{tvg_id}"',
            f'tvg-name="{full_display_title}"',
            f'tvg-logo="{logo}"',
            f'group-title="{group}"'
        ]
        if lang:
            extinf_parts.append(f'tvg-language="{lang}"')
        if country:
            extinf_parts.append(f'tvg-country="{country}"')
        
        extinf_line = " ".join(extinf_parts) + f",{full_display_title}"
        lines.append(extinf_line)
        lines.append(f"#EXTGRP:{group}")
        lines.append(stream_url)
        lines.append("")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Generated: {filepath} ({len(items)} items)")

if __name__ == '__main__':
    build_bilingual_catalogs()
