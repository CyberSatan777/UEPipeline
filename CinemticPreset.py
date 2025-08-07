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
main_seq = asset_tools.create_asset(f"{shot_name}_Main", f"{base_path}/Sequences", None, seq_factory)

# --- Саб-секвенции и добавление в основную ---
sub_seqs = []
for sub in level_names:
    sub_seq = asset_tools.create_asset(f"{shot_name}_{sub}", f"{base_path}/Sequences", None, seq_factory)
    sub_seqs.append(sub_seq.get_path_name())

# --- Добавляем SubSequence Track ---
main_seq_asset = unreal.load_asset(main_seq.get_path_name())
track = main_seq_asset.add_master_track(unreal.MovieSceneSubTrack)
for sub_seq_path in sub_seqs:
    sub_seq_asset = unreal.load_asset(sub_seq_path)
    section = track.add_sequence(sub_seq_asset)
main_seq_asset.save_asset()
