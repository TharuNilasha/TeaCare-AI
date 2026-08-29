DISEASE_ADVISORY_DB = {
    'Anthracnose': {
        'display_name': 'Anthracnose',
        'severity': 'High',
        'severity_color': '#e74c3c',  # Red
        'cause': 'Fungal pathogen (*Colletotrichum theae-sinensis* / *Gloeosporium theae*)',
        'symptoms': [
            'Dark brown to black necrotic spots with reddish-brown borders on leaf surface.',
            'Concentric rings visible on mature leaf lesions.',
            'Severe leaf drop, premature leaf blight, and stem dieback under humid conditions.'
        ],
        'organic_treatment': [
            'Prune and destroy infected leaves, twigs, and plucking surfaces.',
            'Apply Neem oil extract (3-5%) or copper octanoate spray during initial lesion onset.',
            'Improve bush spacing and shade management to enhance air circulation.'
        ],
        'chemical_treatment': [
            'Foliar spray of Copper Oxychloride (0.25%) or Carbendazim (0.1%).',
            'Alternate systemic fungicides like Azoxystrobin (23% SC) or Difenoconazole to prevent resistance.'
        ],
        'prevention': [
            'Avoid overhead irrigation during high humidity periods.',
            'Maintain balanced potash fertilization to strengthen leaf cell walls.',
            'Sanitize plucking tools regularly.'
        ]
    },
    'Algal Leaf Spot': {
        'display_name': 'Algal Leaf Spot',
        'severity': 'Moderate',
        'severity_color': '#e67e22',  # Orange
        'cause': 'Parasitic green alga (*Cephaleuros virescens*)',
        'symptoms': [
            'Circular, raised velvet-like spots ranging from orange-red to grayish-green on upper leaf blade.',
            'Chlorosis around spots, leading to premature leaf shedding.',
            'Stem cankers under severe infestation weakening tea bushes.'
        ],
        'organic_treatment': [
            'Prune overgrown canopy branches to reduce moisture trapping.',
            'Spray Bordeaux mixture (1%) or copper soap fungicides.',
            'Remove severely affected lower leaves.'
        ],
        'chemical_treatment': [
            'Copper Oxychloride 50% WP (2.5 g/L) spray after plucking.',
            'Mancozeb 75% WP (2 g/L) applications during monsoon transitions.'
        ],
        'prevention': [
            'Ensure adequate field drainage and weed control.',
            'Avoid excessive nitrogen fertilization without balanced potassium.',
            'Plant shade trees at optimal density.'
        ]
    },
    'Bird\'s Eye Spot': {
        'display_name': 'Bird\'s Eye Spot',
        'severity': 'Moderate',
        'severity_color': '#f39c12',  # Amber
        'cause': 'Fungal pathogen (*Cercospora theae*)',
        'symptoms': [
            'Small circular spots with grayish-white centers and dark brown outer halos resembling a bird\'s eye.',
            'Shot-hole effect where leaf center drops out leaving perforated leaves.',
            'Common in young tea nurseries and flush leaves.'
        ],
        'organic_treatment': [
            'Apply bio-fungicides such as *Trichoderma viride* or *Bacillus subtilis*.',
            'Spray garlic extract or seaweed foliar sprays to boost immunity.',
            'Remove fallen leaf debris around nursery beds.'
        ],
        'chemical_treatment': [
            'Spray Chlorothalonil 75% WP (2.0 g/L) or Mancozeb (2.5 g/L).',
            'Apply Propiconazole 25% EC (1 mL/L) if disease spreads rapidly.'
        ],
        'prevention': [
            'Provide partial shade for young tea seedlings.',
            'Avoid overwatering nursery beds.',
            'Maintain field sanitation.'
        ]
    },
    'Brown Blight': {
        'display_name': 'Brown Blight',
        'severity': 'High',
        'severity_color': '#c0392b',  # Dark Red
        'cause': 'Fungal pathogen (*Colletotrichum camelliae* / *Glomerella cingulata*)',
        'symptoms': [
            'Large chocolate-brown to reddish-brown patches spreading from leaf margins or tips.',
            'Tiny black fruiting bodies (acervuli) visible on upper lesion surface.',
            'Brittle leaf tissue causing edge tearing and significant leaf loss.'
        ],
        'organic_treatment': [
            'Remove blighted leaves and burn diseased prunings.',
            'Apply Copper Hydroxide or liquid bio-sulfur spray.',
            'Maintain organic mulch to regulate soil moisture.'
        ],
        'chemical_treatment': [
            'Spray Hexaconazole 5% EC (1 mL/L) or Carbendazim 50% WP (1 g/L).',
            'Foliar spray with Copper Oxychloride (2.5 g/L) post-harvest.'
        ],
        'prevention': [
            'Prevent leaf injury during mechanical plucking.',
            'Ensure proper spacing between bushes for canopy ventilation.',
            'Apply balanced NPK fertilizer with adequate Potassium.'
        ]
    },
    'Gray Light': {
        'display_name': 'Gray Light / Grey Blight',
        'severity': 'High',
        'severity_color': '#d35400',  # Burnt Orange
        'cause': 'Fungal pathogen (*Pestalotiopsis theae* / *Pestalotia*)',
        'symptoms': [
            'Irregular grayish-white to silvery spots with dark brown wavy concentric rings.',
            'Black dot-like spore masses visible on mature gray spots.',
            'Leaves dry out and crack along affected margins.'
        ],
        'organic_treatment': [
            'Prune affected shoots 2-3 inches below infected area.',
            'Foliar application of *Trichoderma harzianum* formulation.',
            'Use compost tea and micronutrient sprays to build plant vigor.'
        ],
        'chemical_treatment': [
            'Spray Carbendazim + Mancozeb combination (2 g/L).',
            'Apply Tebuconazole + Trifloxystrobin for systemic protection.'
        ],
        'prevention': [
            'Protect leaves from sun scald and hail damage.',
            'Sanitize pruning knives between bushes.',
            'Avoid nitrogen over-fertilization.'
        ]
    },
    'Healthy Tea Leaf': {
        'display_name': 'Healthy Tea Leaf',
        'severity': 'None',
        'severity_color': '#2ecc71',  # Green
        'cause': 'No pathogen detected (Vigorous foliage)',
        'symptoms': [
            'Deep green, glossy leaf blade with uniform texture.',
            'No necrotic spots, discoloration, or algal growth.',
            'Optimal leaf structure and healthy vein network.'
        ],
        'organic_treatment': [
            'Maintain regular organic soil enrichment with vermicompost.',
            'Routine spray of neem leaf extract for preventative pest deterrence.'
        ],
        'chemical_treatment': [
            'No chemical fungicides required.',
            'Maintain standard NPK nutrient management schedule.'
        ],
        'prevention': [
            'Continue regular crop monitoring and weed management.',
            'Maintain optimal soil pH (4.5 - 5.5) suitable for tea growth.',
            'Ensure balanced field irrigation and drainage.'
        ]
    },
    'Red Leaf Spot': {
        'display_name': 'Red Leaf Spot',
        'severity': 'Moderate',
        'severity_color': '#e74c3c',  # Red
        'cause': 'Fungal pathogen (*Phoma spp.* / *Cephaleuros*)',
        'symptoms': [
            'Distinct reddish-brown to dark red circular spots on leaf surface.',
            'Lesions cause leaf puckering and yellowing of adjacent lamina.',
            'May cause premature defoliation under high heat and moisture.'
        ],
        'organic_treatment': [
            'Apply copper octanoate or sulfur-based organic fungicide.',
            'Prune heavily infested twigs and clear underbrush.',
            'Foliar spray of neem seed kernel extract (NSKE 5%).'
        ],
        'chemical_treatment': [
            'Spray Mancozeb (2.5 g/L) or Copper Oxychloride (2.5 g/L).',
            'Use Difenoconazole 25% EC (0.5 mL/L) for severe infections.'
        ],
        'prevention': [
            'Ensure good drainage in low-lying plantation areas.',
            'Avoid physical leaf wounding.',
            'Maintain optimal shade canopy density.'
        ]
    },
    'White Spot': {
        'display_name': 'White Spot',
        'severity': 'Low-Moderate',
        'severity_color': '#3498db',  # Blue
        'cause': 'Fungal pathogen (*Phyllosticta theae*)',
        'symptoms': [
            'Small round bleached white or pale straw-colored spots with thin dark brown borders.',
            'Center of lesions becomes thin, papery, and brittle.',
            'Mild defoliation in shade-starved or stressed tea bushes.'
        ],
        'organic_treatment': [
            'Apply liquid copper fungicide or sulfur powder.',
            'Prune dense lower branches to increase sunlight exposure.',
            'Spray liquid bio-fertilizer to promote new shoot growth.'
        ],
        'chemical_treatment': [
            'Foliar spray of Chlorothalonil (2 g/L) or Zineb (2.5 g/L).',
            'Spray Carbendazim (1 g/L) if spots spread across plucking table.'
        ],
        'prevention': [
            'Maintain proper bush pruning cycle.',
            'Avoid waterlogging around bush base.',
            'Balance shade tree foliage to prevent over-shading.'
        ]
    }
}

def get_disease_advisory(class_key):
    """
    Returns advisory dictionary for a given class key.
    """
    return DISEASE_ADVISORY_DB.get(class_key, DISEASE_ADVISORY_DB['Healthy Tea Leaf'])

