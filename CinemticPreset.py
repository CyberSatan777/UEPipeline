import unreal

# --- Настройки ---
shot_name = "Shot_010"
base_path = f"/Game/Cinematics/{shot_name}"
level_names = ["GEO", "LGHT", "FX", "CHR"]

# --- Создаём папки ---
unreal.EditorAssetLibrary.make_directory(f"{base_path}/Levels")
unreal.EditorAssetLibrary.make_directory(f"{base_path}/Sequences")

# --- Создаём основной левел ---
level_tools = unreal.LevelEditorSubsystem()
main_level_path = f"{base_path}/Levels/{shot_name}_Main"
main_level = level_tools.new_level_from_template(main_level_path, "/Engine/Maps/Templates/Template_Default")

# --- Саб-левелы ---
sub_levels = []
for sub in level_names:
    sub_level_path = f"{base_path}/Levels/{shot_name}_{sub}"
    sub_level = level_tools.new_level_from_template(sub_level_path, "/Engine/Maps/Templates/Template_Default")
    sub_levels.append(sub_level_path)

# --- Подключаем саб-левелы к основному (Level Streaming) ---
world = unreal.EditorLoadingAndSavingUtils.load_map(main_level_path)
ls = unreal.LevelStreamingDynamic
for sub_level in sub_levels:
    unreal.EditorLevelUtils.add_level_to_world(world, sub_level, ls)

# --- Создаём секвенции ---
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
seq_factory = unreal.LevelSequenceFactoryNew()

# Создаём основную секвенцию и сразу сохраняем
main_seq = asset_tools.create_asset(f"{shot_name}_Main", f"{base_path}/Sequences", None, seq_factory)
unreal.EditorAssetLibrary.save_loaded_asset(main_seq)

# Добавляем трек для саб-секвенций
track = main_seq.add_master_track(unreal.MovieSceneSubTrack)

# Создаём саб-секвенции, сохраняем и добавляем в трек основной секвенции
for sub in level_names:
    sub_seq = asset_tools.create_asset(f"{shot_name}_{sub}", f"{base_path}/Sequences", None, seq_factory)
    unreal.EditorAssetLibrary.save_loaded_asset(sub_seq)
    track.add_sequence(sub_seq)

# Сохраняем основную секвенцию с добавленными саб-секвенциями
unreal.EditorAssetLibrary.save_loaded_asset(main_seq)
