/* The data vocabulary, for display only.

   Country, region, crop, outcome, practice and comparator values come from the
   controlled vocabulary of the source syntheses. They are stored in English,
   filtered in English, and DOWNLOADED IN ENGLISH. This file only changes what
   the reader sees, so a CSV taken from the Spanish site is identical to one
   taken from the English site.

   A term with no entry falls back to English, so an incomplete list still
   gives a working page.

   Scientific binomials (Gmelina arborea, Sesbania sesban, Tephrosia vogelii,
   Mucuna pruriens) and index names (Shannon, Simpson, Chao1) are the same in
   every language and are left alone.

   Spanish uses the Latin American register, not Spain's: costos not costes,
   mani not cacahuete, papa not patata. That follows where the Hub's Spanish
   readers and its host institution are.

   Terms were chosen against what the data actually holds, not word by word.
   Intercropping is 'cultivos asociados' because the records are mixed stands,
   not only row intercropping. Tillage is 'travail du sol', not 'labour',
   which would mean ploughing specifically. Land Equivalent Ratio keeps its
   LER acronym in both languages, because that is what people search for.

   Still worth an agronomist's eye before the site is promoted. Terminology is
   the review team's call: correct a term here and it changes everywhere it
   appears. */

window.KH_VOCAB = {

  es: {
    /* countries */
    'Ethiopia': 'Etiopía', 'India': 'India', 'Kenya': 'Kenia', 'Malawi': 'Malawi',
    'Mexico': 'México', 'Peru': 'Perú', 'South Africa': 'Sudáfrica',
    'Tunisia': 'Túnez', 'Zambia': 'Zambia',

    /* regions */
    'Central America': 'América Central', 'Eastern Africa': 'África Oriental',
    'Northern Africa': 'África del Norte', 'South America': 'América del Sur',
    'South-eastern Asia': 'Sudeste Asiático', 'Southern Africa': 'África Austral',
    'Southern Asia': 'Asia Meridional',
    'Middle Africa': 'África Central',
    'Western Africa': 'África Occidental',
    'Northern America': 'América del Norte',
    'Caribbean': 'Caribe',
    'Western Asia': 'Asia Occidental',
    'Central Asia': 'Asia Central',
    'Eastern Asia': 'Asia Oriental',
    'Northern Europe': 'Europa del Norte',
    'Western Europe': 'Europa Occidental',
    'Southern Europe': 'Europa del Sur',
    'Eastern Europe': 'Europa del Este',
    'Oceania': 'Oceanía',

    /* outcomes */
    'Abundance': 'Abundancia', 'Costs': 'Costos', 'Diversity Index': 'Índice de diversidad',
    'Dominance index': 'Índice de dominancia', 'Economic Performance': 'Resultados económicos',
    'Efficiency': 'Eficiencia', 'Evenness Index': 'Índice de equidad', 'Income': 'Ingresos',
    'Organism Biomass': 'Biomasa de organismos', 'Pest & Pathogen': 'Plagas y patógenos',
    'Product Yield': 'Rendimiento', 'Richness': 'Riqueza',
    'Richness Estimator': 'Estimador de riqueza', 'Soil Quality': 'Calidad del suelo',

    /* practices and comparators */
    'Agroforestry': 'Agroforestería', 'Bare Fallow': 'Barbecho desnudo',
    'Conventional Tillage': 'Labranza convencional', 'Crop rotation': 'Rotación de cultivos',
    'Improved Fallow': 'Barbecho mejorado', 'Insects control': 'Control de insectos',
    'Intercropping': 'Cultivos asociados', 'Monoculture': 'Monocultivo',
    'No Fertilizers Applied': 'Sin aplicación de fertilizantes', 'Reduced Tillage': 'Labranza reducida',
    'Semi-natural habitat': 'Hábitat seminatural', 'Simple intercropping': 'Asociación simple de cultivos',
    'External input dependency': 'Dependencia de insumos externos', 'Inoculants': 'Inoculantes',
    'Natural habitat': 'Hábitat natural', 'Timber plantation': 'Plantación maderera',
    'Zero Tillage': 'Siembra directa',

    /* crops */
    'Baby Corn': 'Maíz baby', 'Cassava': 'Yuca', 'Castor': 'Ricino', 'Cauliflower': 'Coliflor',
    'Cocoa': 'Cacao', 'Coffee': 'Café', 'Common Bean': 'Frijol común', 'Cowpea': 'Caupí',
    'Fava Bean': 'Haba', 'Groundnut': 'Maní', 'Jack Bean/Maize': 'Canavalia/Maíz',
    'Maize': 'Maíz',
    'Maize/Grass Unspecified/Native legumes': 'Maíz/Gramínea sin especificar/Leguminosas nativas',
    'Maize/Pigeon Pea': 'Maíz/Gandul', 'Maize/Sesbania sesban': 'Maíz/Sesbania sesban',
    'Maize/Tephrosia vogelii': 'Maíz/Tephrosia vogelii', 'Mandarin Orange': 'Mandarina',
    'Mango': 'Mango', 'Mucuna pruriens/Maize': 'Mucuna pruriens/Maíz', 'Onion': 'Cebolla',
    'Pearl Millet': 'Mijo perla', 'Pigeon Pea': 'Gandul', 'Pineapple': 'Piña', 'Potato': 'Papa',
    'Rice/Maize/Rice': 'Arroz/Maíz/Arroz', 'Rice/Mung Bean/Maize': 'Arroz/Frijol mungo/Maíz',
    'Rice/Mung Bean/Rice': 'Arroz/Frijol mungo/Arroz', 'Sorghum': 'Sorgo', 'Tomato': 'Tomate',
    'Unspecified Tree': 'Árbol sin especificar',

    /* sub-indicators, shown in the record panel */
    'Benefit Cost Ratio (GRTC)': 'Relación beneficio-costo (GRTC)',
    'Benefit Cost Ratio (NRTC)': 'Relación beneficio-costo (NRTC)',
    'Benefit Cost Ratio (Unspecified)': 'Relación beneficio-costo (sin especificar)',
    'Berger-Parker dominance (d)': 'Dominancia de Berger-Parker (d)',
    'Biomass Yield': 'Rendimiento de biomasa', 'Chao1 Index': 'Índice Chao1',
    'Colonisation percent': 'Porcentaje de colonización', 'Crop Yield': 'Rendimiento del cultivo',
    'Damage caused by pest': 'Daño causado por plagas',
    'Energy Use Efficiency': 'Eficiencia energética', 'Erosion': 'Erosión',
    'Fisher Alpha': 'Alfa de Fisher', 'Gross Return': 'Ingreso bruto',
    'Jack-knife Species Richness': 'Riqueza de especies (jack-knife)',
    'Land Equivalent Ratio': 'Índice equivalente de tierra (LER)',
    'Microbial biomass': 'Biomasa microbiana', 'Net Present Value': 'Valor actual neto',
    'Net Return': 'Ingreso neto', 'Rarefied Species Richness': 'Riqueza de especies rarificada',
    'Runoff': 'Escorrentía', 'Shannon Index': 'Índice de Shannon',
    'Shannon-Wiener Index': 'Índice de Shannon-Wiener', 'Simpson Index': 'Índice de Simpson',
    'Soil Available Nitrogen': 'Nitrógeno disponible en el suelo',
    'Soil Available Phosphorus': 'Fósforo disponible en el suelo',
    'Soil Available Potassium': 'Potasio disponible en el suelo',
    'Soil Moisture': 'Humedad del suelo', 'Soil Organic Carbon': 'Carbono orgánico del suelo',
    'Species Evenness': 'Equidad de especies', 'Species Richness': 'Riqueza de especies',
    'Total Cost': 'Costo total', 'Water Use Efficiency': 'Eficiencia en el uso del agua'
  },

  fr: {
    /* countries */
    'Colombia': 'Colombie', 'Ethiopia': 'Éthiopie', 'India': 'Inde', 'Kenya': 'Kenya',
    'Mexico': 'Mexique', 'Peru': 'Pérou', 'South Africa': 'Afrique du Sud',
    'Tunisia': 'Tunisie', 'Vietnam': 'Viêt Nam', 'Zambia': 'Zambie',

    /* regions */
    'Central America': 'Amérique centrale', 'Eastern Africa': 'Afrique de l’Est',
    'Northern Africa': 'Afrique du Nord', 'South America': 'Amérique du Sud',
    'South-eastern Asia': 'Asie du Sud-Est', 'Southern Africa': 'Afrique australe',
    'Southern Asia': 'Asie du Sud',
    'Middle Africa': 'Afrique centrale',
    'Western Africa': 'Afrique de l’Ouest',
    'Northern America': 'Amérique du Nord',
    'Caribbean': 'Caraïbes',
    'Western Asia': 'Asie de l’Ouest',
    'Central Asia': 'Asie centrale',
    'Eastern Asia': 'Asie de l’Est',
    'Northern Europe': 'Europe du Nord',
    'Western Europe': 'Europe de l’Ouest',
    'Southern Europe': 'Europe du Sud',
    'Eastern Europe': 'Europe de l’Est',
    'Oceania': 'Océanie',

    /* outcomes */
    'Abundance': 'Abondance', 'Costs': 'Coûts', 'Diversity Index': 'Indice de diversité',
    'Dominance index': 'Indice de dominance', 'Economic Performance': 'Performance économique',
    'Efficiency': 'Efficience', 'Evenness Index': 'Indice d’équitabilité', 'Income': 'Revenu',
    'Organism Biomass': 'Biomasse des organismes', 'Pest & Pathogen': 'Ravageurs et pathogènes',
    'Product Yield': 'Rendement', 'Richness': 'Richesse',
    'Richness Estimator': 'Estimateur de richesse', 'Soil Quality': 'Qualité du sol',

    /* practices and comparators */
    'Agroforestry': 'Agroforesterie', 'Bare Fallow': 'Jachère nue',
    'Conventional Tillage': 'Travail du sol conventionnel', 'Crop rotation': 'Rotation des cultures',
    'Improved Fallow': 'Jachère améliorée', 'Insects control': 'Lutte contre les insectes',
    'Intercropping': 'Cultures associées', 'Monoculture': 'Monoculture',
    'No Fertilizers Applied': 'Sans apport d’engrais', 'Reduced Tillage': 'Travail du sol réduit',
    'Semi-natural habitat': 'Habitat semi-naturel',
    'Simple intercropping': 'Cultures associées simples',
    'External input dependency': 'Dépendance aux intrants externes', 'Inoculants': 'Inoculants',
    'Natural habitat': 'Habitat naturel', 'Timber plantation': 'Plantation forestière',
    'Zero Tillage': 'Semis direct',

    /* crops */
    'Baby Corn': 'Maïs miniature', 'Cassava': 'Manioc', 'Castor': 'Ricin',
    'Cauliflower': 'Chou-fleur', 'Cocoa': 'Cacao', 'Coffee': 'Café',
    'Common Bean': 'Haricot commun', 'Cowpea': 'Niébé', 'Fava Bean': 'Fève',
    'Groundnut': 'Arachide', 'Jack Bean/Maize': 'Pois sabre/Maïs', 'Maize': 'Maïs',
    'Maize/Grass Unspecified/Native legumes': 'Maïs/Graminée non précisée/Légumineuses locales',
    'Maize/Pigeon Pea': 'Maïs/Pois d’Angole', 'Maize/Sesbania sesban': 'Maïs/Sesbania sesban',
    'Maize/Tephrosia vogelii': 'Maïs/Tephrosia vogelii', 'Mandarin Orange': 'Mandarine',
    'Mango': 'Mangue', 'Mucuna pruriens/Maize': 'Mucuna pruriens/Maïs', 'Onion': 'Oignon',
    'Pearl Millet': 'Mil à chandelle', 'Pigeon Pea': 'Pois d’Angole', 'Pineapple': 'Ananas',
    'Potato': 'Pomme de terre', 'Rice/Maize/Rice': 'Riz/Maïs/Riz',
    'Rice/Mung Bean/Maize': 'Riz/Haricot mungo/Maïs', 'Rice/Mung Bean/Rice': 'Riz/Haricot mungo/Riz',
    'Sorghum': 'Sorgho', 'Tomato': 'Tomate', 'Unspecified Tree': 'Arbre non précisé',

    /* sub-indicators, shown in the record panel */
    'Benefit Cost Ratio (GRTC)': 'Rapport bénéfice-coût (GRTC)',
    'Benefit Cost Ratio (NRTC)': 'Rapport bénéfice-coût (NRTC)',
    'Benefit Cost Ratio (Unspecified)': 'Rapport bénéfice-coût (non précisé)',
    'Berger-Parker dominance (d)': 'Dominance de Berger-Parker (d)',
    'Biomass Yield': 'Rendement en biomasse', 'Chao1 Index': 'Indice Chao1',
    'Colonisation percent': 'Pourcentage de colonisation', 'Crop Yield': 'Rendement de la culture',
    'Damage caused by pest': 'Dégâts causés par les ravageurs',
    'Energy Use Efficiency': 'Efficience énergétique', 'Erosion': 'Érosion',
    'Fisher Alpha': 'Alpha de Fisher', 'Gross Return': 'Produit brut',
    'Jack-knife Species Richness': 'Richesse spécifique (jack-knife)',
    'Land Equivalent Ratio': 'Rapport de surface équivalente (LER)',
    'Microbial biomass': 'Biomasse microbienne', 'Net Present Value': 'Valeur actuelle nette',
    'Net Return': 'Produit net', 'Rarefied Species Richness': 'Richesse spécifique raréfiée',
    'Runoff': 'Ruissellement', 'Shannon Index': 'Indice de Shannon',
    'Shannon-Wiener Index': 'Indice de Shannon-Wiener', 'Simpson Index': 'Indice de Simpson',
    'Soil Available Nitrogen': 'Azote disponible du sol',
    'Soil Available Phosphorus': 'Phosphore disponible du sol',
    'Soil Available Potassium': 'Potassium disponible du sol',
    'Soil Moisture': 'Humidité du sol', 'Soil Organic Carbon': 'Carbone organique du sol',
    'Species Evenness': 'Équitabilité spécifique', 'Species Richness': 'Richesse spécifique',
    'Total Cost': 'Coût total', 'Water Use Efficiency': 'Efficience d’utilisation de l’eau'
  }
};
