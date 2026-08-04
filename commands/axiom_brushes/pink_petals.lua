-- Check if target block is air
if getBlock(x, y, z) ~= blocks.air then
	return nil
end

-- Check if a solid block is below
if not isSolid(getBlockState(x, y-1, z)) then
	return nil
end

-- Load custom arguments
local grassiness = $float(Grassiness, 0.5, 0.0, 1.0)$
local short_grass = $blockState(Short, short_grass)$

-- Base condition for grassiness
if math.random() > grassiness then
	return nil
end

-- Calculate noise values
local simplex = getSimplexNoise(x/12, y/12, z/12)
local white = math.random()
local transformed
if white < 0.5 then
	transformed = math.sqrt(white / 2)
else
	transformed = 1 - math.sqrt((1 - white)/2)
end

-- On charge le bloc d'herbe de sol pour la comparaison via le système '$'
local grass_block = $blockState(GrassBlock, grass_block)$

-- Ta condition corrigée
if simplex < transformed and getBlockState(x, y-1, z) == grass_block then
	-- Génération d'un index aléatoire (de 1 à 4)
	local r = math.random(1, 4)

	-- Renvoie les pétales avec le bon amount sur les blocs d'herbe
	if r == 1 then return blocks.pink_petals end
	if r == 2 then return blocks.pink_petals end
	if r == 3 then return blocks.pink_petals end
	return blocks.pink_petals
end