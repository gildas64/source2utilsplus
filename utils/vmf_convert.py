# cmd command: python vmf_convert.py "C:\path\to\vmf\file.vmf"

import re
import sys
import os

global classnameVar, saveLines, savingProces, deletingProces, ObseleteEntities, saveSolidLines, savingSolidProces


def LogPrint(inputString, print_bool=True):
    logFile.write(inputString + '\n')
    if print_bool == True:
        print(inputString)


INPUT_FILE_EXT = '.vmf'

print('--------------------------------------------------------------------------------------------------------')
print('Source 2 .vmf Prepper! EXPERIMENTAL!! By "caseytube", "The [G]amerX" and "pack" <3 via Github')
print('Converts .vmf files to be ready for Source 2 by fixing materials and entities')
print('--------------------------------------------------------------------------------------------------------')

#############################################################

PATH_TO_VMF = (len(sys.argv) == 2 and sys.argv[1] or input("What folder would you like to convert? Choose .vmf file\n")).lower()

someInput = input("Would you like to convert/delete 'weapon_*' entities?\n - 1: convert weapons entities\n - 2: delete weapons entities\n - 3: make them prop_physics with the appropriate model \n (1/2/3):").lower()
if someInput in "1":
    convert_weapons = 1
elif someInput in "2":
    convert_weapons = 2
elif someInput in "3":
    convert_weapons = 3
else:
    print("Please respond with '1', '2' or '3'. Quitting process!")
    quit()

#############################################################

someInput = input("Would you like to delete Player Clip brushes? (y/n):").lower()
if someInput in "yes":
    deletePlayerClips = 1
elif someInput in "no":
    deletePlayerClips = 0
else:
    print("Please respond with 'yes' or 'no'. Quitting process!")
    quit()

#############################################################

someInput = input("Would you like to delete Clip brushes? (y/n):").lower()
if someInput in "yes":
    deleteClips = 1
elif someInput in "no":
    deleteClips = 0
else:
    print("Please respond with 'yes' or 'no'. Quitting process!")
    quit()

#############################################################

filename = PATH_TO_VMF
convertedFilename = filename.replace(INPUT_FILE_EXT, '') + 'Converted' + INPUT_FILE_EXT
LogFilename = filename.replace(INPUT_FILE_EXT, '') + '_log.txt'
logFile = open(LogFilename, 'w')

if not os.path.exists(filename):
    print("input file doesn't exist")
    quit()

LogPrint('Importing ' + os.path.basename(filename))

deletingProces = 0
savingProces = 0
savingSolidProces = 0
classnameVar = ""
saveLines = ""
saveSolidLines = ""
EntitiesToConvert = {
    "\"env_volumetric_fog_volume\"": {"fog_volume"},
    "\"env_volumetric_fog_controller\"": {"env_fog_controller"},
    "\"env_sky\"": {"env_sun"},
    "\"info_hlvr_equip_player\"": {"game_player_equip"},
    "\"info_player_start\"": {
        "\"info_player_terrorist\"",
        "\"info_player_counterterrorist\"",
        "\"info_player_teamspawn\"",
        "\"info_player_deathmatch\""
    },
    "\"item_item_crate\"": {
        "\"prop_loot_crate\"",
        "\"prop_metal_crate\"",
        "\"prop_money_crate\"",
        "\"prop_paradrop_crate\"",
        "\"point_dz_weaponspawn\"",
        "\"point_dz_itemspawn\""
    },
    "\"func_brush\"": {
        "\"func_conveyor\"",
        "\"func_detail_blocker\"",
        "\"func_occluder\""
    },
    "\"weapon_pistol\"": {
        "\"weapon_deagle\"",
        "\"weapon_usp\"",
        "\"weapon_p250\"",
        "\"weapon_fiveseven\"",
        "\"weapon_hpk\"",
        "\"weapon_glock\""
    },
    "\"weapon_shotgun\"": {
        "\"weapon_xm1014\"",
        "\"weapon_autoshotgun\"",
        "\"weapon_mag7\"",
        "\"weapon_sawedoff\"",
        "\"weapon_m13\""
    },
    "\"weapon_ar2\"": {
        "\"weapon_ak47\"",
        "\"weapon_m4a1\"",
        "\"weapon_galil\"",
        "\"weapon_famas\"",
        "\"weapon_aug\""
    },
    "\"weapon_crowbar\"": {
        "\"weapon_knife\"",
        "\"weapon_bayonet\"",
        "\"weapon_hammer\"",
        "\"weapon_axe\"",
        "\"weapon_spanner\"",
        "\"weapon_melee\""
    },
    "\"weapon_357\"": {"\"weapon_revolver\""},
    "\"item_healthvial\"": {"\"weapon_healthshot\""},
    "\"item_hlvr_weapon_tripmine\"": {"\"weapon_breachcharge\""},
    "\"weapon_frag\"": {"\"weapon_hegrenade\""},
    "\"npc_turret_floor\"": {
        "\"dronegun\"",
        "\"point_dz_dronegun\""
    },
    "\"prop_door_rotating\"": {"\"dz_door\""},
    "\"prop_physics\"": {"\"prop_physics_multiplayer\""},
}
ObseleteEntities = [
    "\"func_areaportal\"",
    "\"func_areaportalwindow\"",
    "\"postprocess_controller\"",
    "\"env_detail_controller\"",
    "\"shadow_control\"",
    "\"func_fish_pool\"",
    "\"fish\"",
    "\"pet_entity\"",
    "\"chicken\"",
    "\"func_no_defuse\"",
    "\"env_tonemap_controller_ghost\"",
    "\"env_tonemap_controller_infected\"",
    "\"prop_mapplaced_long_use_entity\"",
    "\"item_dogtags\"",
    "\"item_heavyassaultsuit\"",
    "\"item_cutters\"",
    "\"item_defuser\"",
    "\"prop_weapon_upgrade_tablet_droneintel\"",
    "\"prop_weapon_upgrade_tablet_highres\"",
    "\"prop_weapon_upgrade_tablet_zoneintel\"",
    "\"hostage\"",
    "\"hostage_entity\"",
    "\"info_hostage_spawn\"",
    "\"hostage_carriable_prop\"",
    "\"info_hostage_rescue_zone_hint\"",
    "\"inferno\"",
    "\"weapon_gascan\"",
    "\"weapon_zone_repulsor\"",
    "\"ability_selfdestruct\"",
    "\"ent_snowball_pile\"",
    "\"item_assaultsuit\"",
    "\"item_cash\"",
    "\"item_coop_coin\"",
    "\"trigger_survival_playarea\"",
    "\"info_gascanister_launchpoint\"",
    "\"info_map_parameters\"",
    "\"water_lod_control\"",
    "\"logic_eventlistener\"",
    "\"game_survival_logic\"",
    "\"info_map_region\"",
    "\"func_tablet_blocker\"",
    "\"func_survival_c4_target\"",
    "\"prop_counter\"",
    "\"func_bomb_target\"",
    "\"func_hostage_rescue\"",
    "\"func_clip_vphysics\"",
    "_projectile\""
]

if convert_weapons == 2:
    ObseleteEntities.append("\"weapon_")
with open(convertedFilename, 'w') as convFile:
    with open(filename, 'r') as vmfFile:
        for line in vmfFile.readlines():
            splitLine = line.replace('"', '').replace("'", "").split()
            last = len(splitLine) - 1

            #############################################################

            if 1 == savingProces:
                if "\"classname\"" not in line:
                    saveLines = saveLines + line
                    continue

            if "entity\n" == line:
                savingProces = 1
                saveLines = line
                continue

            if "\"classname\"" in line:
                classnameVar = splitLine[last]
                ForDelete = 0
                for ObseleteEntity in ObseleteEntities:
                    if ObseleteEntity in line:
                        ForDelete = 1
                        break
                if ForDelete == 1:
                    LogPrint(' --> Deleting ' + str(classnameVar) + ' entity.')
                    deletingProces = 1
                    savingProces = 0
                    saveLines = ""
                    continue
                else:
                    LogPrint(' --> Checking ' + str(classnameVar) + ' entity.')
                    convFile.write(saveLines)
                    deletingProces = 0
                    savingProces = 0
                    saveLines = ""

            if 1 == deletingProces:
                if "}" == line:
                    deletingProces = 0
                continue

            #############################################################

            if 1 == savingSolidProces:
                if "\"material\"" in line:
                    if "\"TOOLS/TOOLSDRONECLIP\"" in line:
                        saveSolidLines = saveSolidLines + line
                        continue
                    elif 1 == deletePlayerClips and "\"TOOLS/TOOLSPLAYERCLIP\"" in line:
                        saveSolidLines = saveSolidLines + line
                        continue
                    elif 1 == deleteClips and "\"TOOLS/TOOLSCLIP\"" in line:
                        saveSolidLines = saveSolidLines + line
                        continue
                    else:
                        convFile.write(saveSolidLines)
                        savingSolidProces = 0
                        saveSolidLines = ""
                elif "	}\n" == line:
                    LogPrint(' -> Deleting Clip brush.')
                    savingSolidProces = 0
                    saveSolidLines = ""
                    continue
                else:
                    saveSolidLines = saveSolidLines + line
                    continue

            if "worldspawn" in classnameVar:
                if "	solid\n" == line:
                    savingSolidProces = 1
                    saveSolidLines = line
                    continue

            #############################################################

            bLineFound = False
            for ResultClass in EntitiesToConvert:
                for EntityClass in EntitiesToConvert[ResultClass]:
                    if EntityClass in line:
                        newLine = line.replace(EntityClass, ResultClass)
                        LogPrint(f'{EntityClass} -> {ResultClass}')
                        convFile.write(newLine)

                        bLineFound = True

            if bLineFound:
                continue

            if "\"uaxis\"" in line or "\"vaxis\"" in line:
                scale = splitLine[last]
                shift = splitLine[last-1].replace("]", "")

                newScale = float(scale) * 32
                newShift = float(shift) / 32

                oldLine = re.split('\-?[0-9]\d{0,2}(\.\d*||)\]', line)
                newLine = oldLine[0] + str(newShift) + '] ' + str(newScale) + "\"\n"

                convFile.write(newLine)
            elif "\"uniformscale\"" in line:
                oldVar = splitLine[last]
                newLine = line.replace("uniformscale", "scales")
                newLine = newLine.replace(str(oldVar), f'{str(oldVar)} {str(oldVar)} {str(oldVar)}')
                convFile.write(newLine)
            elif "\"fogend\"" in line:
                newLine = line.replace("fogend", "FadeInEnd")
                LogPrint('Fixing "fogend" property...')
                convFile.write(newLine)
            elif "\"fogstart\"" in line:
                newLine = line.replace("fogstart", "FadeInStart")
                LogPrint('Fixing "fogstart" property...')
                convFile.write(newLine)
            elif "\"fogmaxdensity\"" in line:
                newLine = line.replace("fogmaxdensity", "FogStrength")
                LogPrint('Fixing "fogmaxdensity" property...')
                convFile.write(newLine)
            elif "\"fogenable\"" in line:
                oldVar = splitLine[last]
                newVar = int(oldVar) ^ 1
                newLine = line.replace("fogenable", "StartDisabled")
                LogPrint('Fixing "fogenable" property...')
                newLine = newLine.replace(str(oldVar), str(newVar))
                convFile.write(newLine)
            elif "\"foglerptime\"" in line:
                newLine = line.replace("foglerptime", "FadeSpeed")
                LogPrint('Fixing "foglerptime" property...')
                convFile.write(newLine)
            elif "\"info_teleport_destination\"" in line:
                newLine = line.replace(
                    "info_teleport_destination", "point_teleport")
                LogPrint('info_teleport_destination -> point_teleport')
                convFile.write(newLine)
            elif "\"_inner_cone\"" in line:
                convFile.write(line)
                newLine = line.replace(
                    "_inner_cone", "original_innerconeangle")
                LogPrint('Saving "_inner_cone" property...')
                convFile.write(newLine)
            elif "\"_cone\"" in line:
                convFile.write(line)
                newLine = line.replace("_cone", "original_outerconeangle")
                LogPrint('Saving "_cone" property...')
                convFile.write(newLine)
            elif "\"_linear_attn\"" in line:
                convFile.write(line)
                newLine = line.replace("_linear_attn", "original_attenuation1")
                LogPrint('Saving "_linear_attn" property...')
                convFile.write(newLine)
            elif "\"_quadratic_attn\"" in line:
                convFile.write(line)
                newLine = line.replace(
                    "_quadratic_attn", "original_attenuation2")
                LogPrint('Saving "_quadratic_attn" property...')
                convFile.write(newLine)
            elif "\"_lightHDR\"" in line:
                LogPrint('Skipping "_lightHDR" property...')
            elif "\"_lightscaleHDR\"" in line:
                LogPrint('Skipping "_lightscaleHDR" property...')
            elif "\"_light\"" in line:
                convFile.write(line)
                oldVar = line.replace('"', '').replace("'", "").replace(
                    "_light", "").replace("	 ", "").replace("\n", "")
                LogPrint('Saving "_light" property...')
                R, G, B, A = oldVar.split(' ', 4)
                newA = float(A) * 0.0039215686274509803921568627451
                newLine = line.replace("_light", "original_color")
                newLine = newLine.replace(str(oldVar), f'{str(R)} {str(G)} {str(B)}')
                convFile.write(newLine)
                newLine = line.replace("_light", "original_brightness")
                newLine = newLine.replace(str(oldVar), str(newA))
                convFile.write(newLine)
            elif "\"spawnflags\"" in line:
                if "light_spot" in classnameVar:
                    oldVar = splitLine[last]
                    newVar = int(oldVar) ^ 1
                    newLine = line.replace("spawnflags", "enabled")
                    LogPrint(f'Fixing "spawnflags" property for {classnameVar} entity...')
                    newLine = newLine.replace(str(oldVar), str(newVar))
                    convFile.write(newLine)
                elif "env_tonemap_controller" in classnameVar:
                    newLine = line.replace("spawnflags", "master")
                    LogPrint(f'Fixing "spawnflags" property for {classnameVar} entity...')
                    convFile.write(newLine)
                elif "env_fog_controller" in classnameVar:
                    newLine = line.replace("spawnflags", "IsMaster")
                    LogPrint(f'Fixing "spawnflags" property for {classnameVar} entity...')
                    convFile.write(newLine)
            elif "\"mingpulevel\"" in line:
                if "prop_static" in classnameVar:
                    LogPrint(f'Skipping "mingpulevel" property for {classnameVar} entity...')
            elif "\"mincpulevel\"" in line:
                if "prop_static" in classnameVar:
                    LogPrint(f'Skipping "mincpulevel" property for {classnameVar} entity...')
            elif "\"maxgpulevel\"" in line:
                if "prop_static" in classnameVar:
                    LogPrint(f'Skipping "maxgpulevel" property for {classnameVar} entity...')
            elif "\"maxcpulevel\"" in line:
                if "prop_static" in classnameVar:
                    LogPrint(f'Skipping "maxcpulevel" property for {classnameVar} entity...')
            elif "\"disableX360\"" in line:
                if "prop_static" in classnameVar:
                    LogPrint(f'Skipping "disableX360" property for {classnameVar} entity...')
            elif "\"is_security_door\"" in line:
                if "dz_door" in classnameVar:
                    LogPrint(f'Skipping "is_security_door" property for {classnameVar} entity...')
            elif "\"fademaxdist\"" in line:
                convFile.write(line)
                newLine = line.replace("fademaxdist", "original_fademaxdist")
                LogPrint('Saving "fademaxdist" property...')
                convFile.write(newLine)
            elif "\"fademindist\"" in line:
                convFile.write(line)
                newLine = line.replace("fademindist", "original_fademindist")
                LogPrint('Saving "fademindist" property...')
                convFile.write(newLine)
            elif "\"solid\"" in line:
                convFile.write(line)
                newLine = line.replace("solid", "original_solid")
                LogPrint('Saving "solid" property...')
                convFile.write(newLine)
            elif "\"func_illusionary\"" in line:
                newLine = line.replace("func_illusionary", "func_brush")
                LogPrint('func_illusionary -> func_brush')
                convFile.write(newLine)
                newLine = line.replace("classname", "solid")
                newLine = newLine.replace("func_illusionary", "0")
                convFile.write(newLine)
            elif "\"func_ladderendpoint\"" in line:
                newLine = line.replace(
                    "func_ladderendpoint", "func_useableladder")
                LogPrint('func_ladderendpoint -> func_useableladder')
                convFile.write(newLine)
            elif "\"startsound\"" in line:
                if "func_movelinear" in classnameVar:
                    newLine = line.replace("startsound", "StartSound")
                    LogPrint('Fixing "startsound" property for ' +
                             classnameVar + ' entity...')
                    convFile.write(newLine)
            elif "\"stopsound\"" in line:
                if "func_movelinear" in classnameVar:
                    newLine = line.replace("stopsound", "StopSound")
                    LogPrint('Fixing "stopsound" property for ' +
                             classnameVar + ' entity...')
                    convFile.write(newLine)
            elif "\"teamToBlock\"" in line or "\"affectsFlow\"" in line:
                if "func_nav_blocker" in classnameVar:
                    LogPrint(
                        'Skipping properties for "func_nav_blocker" entity...')
            elif "\"prop_exploding_barrel\"" in line:
                newLine = line.replace("prop_exploding_barrel", "prop_physics")
                LogPrint('prop_exploding_barrel -> prop_physics')
                convFile.write(newLine)
                newLine = line.replace("classname", "model")
                newLine = newLine.replace(
                    "prop_exploding_barrel", "models/props/coop_cementplant/exloding_barrel/exploding_barrel.vmdl")
                convFile.write(newLine)
            else:
                convFile.write(line)
