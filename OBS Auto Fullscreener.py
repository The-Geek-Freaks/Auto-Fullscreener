import obspython as obs
import sys
import platform
import logging
from datetime import datetime

# ------------------------------------------------------------

# Setup logging
def setup_logging():
    log_file = f"obs_projector_{datetime.now().strftime('%Y%m%d')}.log"
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Global variables
script_settings = None
hotkeys = {}
test_projector_active = False
test_scene = None
test_source = None

def start_projector_cb():
    try:
        projector_type = obs.obs_data_get_string(script_settings, "projector_type")
        monitor = obs.obs_data_get_int(script_settings, "monitor")
        selected_scene = obs.obs_data_get_string(script_settings, "scene")
        
        if projector_type == "preview":
            obs.obs_frontend_open_projector("Preview", monitor, "", "")
            logging.info(f"Started preview projector on monitor {monitor + 1}")
        elif projector_type == "scene" and selected_scene:
            obs.obs_frontend_open_projector("Scene", monitor, "", selected_scene)
            logging.info(f"Started scene projector for '{selected_scene}' on monitor {monitor + 1}")
        
        obs.remove_current_callback()
    except Exception as e:
        logging.error(f"Error starting projector: {str(e)}")

def start_test_projector(*args):
    """Start a test projector for 3 seconds"""
    global test_projector_active, test_scene, test_source
    try:
        if test_projector_active:
            return True

        # Get current settings from global variable
        settings = script_settings
        if not settings:
            logging.error("No settings available")
            return True
            
        monitor = obs.obs_data_get_int(settings, "monitor")
        
        # Show a test pattern or text
        test_scene_name = "OBS Projector Test"
        test_source_name = "Test Text"
        
        # Create a temporary scene and source
        test_scene = obs.obs_scene_create(test_scene_name)
        test_source = obs.obs_source_create("text_gdi", test_source_name, None, None)
        
        if test_source and test_scene:
            # Configure test text
            settings = obs.obs_data_create()
            obs.obs_data_set_string(settings, "text", f"Test Projector on Monitor {monitor + 1}\nThis will close in 3 seconds")
            obs.obs_data_set_int(settings, "color", 0xFFFFFFFF)  # White text
            obs.obs_data_set_int(settings, "font_size", 48)
            obs.obs_source_update(test_source, settings)
            obs.obs_data_release(settings)
            
            # Add source to scene
            scene_item = obs.obs_scene_add(test_scene, test_source)
            if scene_item:
                # Center the text
                bounds = obs.vec2()
                obs.obs_source_get_base_width(test_source)
                obs.obs_source_get_base_height(test_source)
                obs.obs_sceneitem_set_alignment(scene_item, 5)  # Center alignment
                
            # Open projector with test scene
            obs.obs_frontend_open_projector("Scene", monitor, "", test_scene_name)
            test_projector_active = True
            
            # Schedule cleanup
            def cleanup():
                global test_projector_active, test_scene, test_source
                try:
                    if test_source:
                        obs.obs_source_remove(test_source)
                        test_source = None
                    if test_scene:
                        obs.obs_scene_release(test_scene)
                        test_scene = None
                    test_projector_active = False
                except Exception as e:
                    logging.error(f"Error in cleanup: {str(e)}")
            
            obs.timer_add(cleanup, 3000)  # 3 seconds
            
            logging.info(f"Started test projector on monitor {monitor + 1}")
        else:
            logging.error("Failed to create test scene or source")
    except Exception as e:
        logging.error(f"Error in test projector: {str(e)}")
        test_projector_active = False
    
    return True

def refresh_scene_list(*args):
    """Callback for refreshing the scene list"""
    try:
        # Get properties from the first argument if available
        props = args[0] if args else None
        if not props:
            logging.error("No properties object available")
            return True

        scene_list = obs.obs_properties_get(props, "scene")
        if not scene_list:
            logging.error("Could not find scene list property")
            return True

        obs.obs_property_list_clear(scene_list)
        
        scenes = get_scene_names()
        for scene in scenes:
            obs.obs_property_list_add_string(scene_list, scene, scene)
        
        logging.info("Scene list refreshed")
    except Exception as e:
        logging.error(f"Error refreshing scene list: {str(e)}")
    
    return True

def on_projector_type_changed(props, property, settings):
    """Show/hide scene selection based on projector type"""
    projector_type = obs.obs_data_get_string(settings, "projector_type")
    scene_prop = obs.obs_properties_get(props, "scene")
    obs.obs_property_set_visible(scene_prop, projector_type == "scene")
    return True

def get_scene_names():
    scenes = obs.obs_frontend_get_scene_names()
    return scenes if scenes else []

def script_load(settings):
    setup_logging()
    logging.info("Script loaded")
    
    # Register hotkeys
    hotkey_id = obs.obs_hotkey_register_frontend(
        "projector_start_trigger",
        "Start Projector",
        start_projector_cb
    )
    hotkey_array = obs.obs_data_get_array(settings, "projector_start_hotkey")
    obs.obs_hotkey_load(hotkey_id, hotkey_array)
    obs.obs_data_array_release(hotkey_array)
    
    hotkeys["projector_start"] = hotkey_id

def script_save(settings):
    """Save hotkey settings"""
    hotkey_array = obs.obs_hotkey_save(hotkeys["projector_start"])
    obs.obs_data_set_array(settings, "projector_start_hotkey", hotkey_array)
    obs.obs_data_array_release(hotkey_array)

def script_unload():
    logging.info("Script unloaded")

def script_update(settings):
    global script_settings
    script_settings = settings
    startup_seconds = obs.obs_data_get_int(settings, "startup_seconds")
    
    if obs.obs_data_get_bool(settings, "start_with_obs"):
        obs.timer_remove(start_projector_cb)
        obs.timer_add(start_projector_cb, startup_seconds * 1000)
        logging.info(f"Scheduled projector start in {startup_seconds} seconds")

def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "startup_seconds", 10)
    obs.obs_data_set_default_int(settings, "monitor", 0)
    obs.obs_data_set_default_string(settings, "projector_type", "preview")
    obs.obs_data_set_default_bool(settings, "start_with_obs", False)

def script_properties():
    props = obs.obs_properties_create()
    
    # Add startup options group
    startup_group = obs.obs_properties_create()
    obs.obs_properties_add_group(props, "startup_group", "Startup Options", obs.OBS_GROUP_NORMAL, startup_group)
    
    auto_start = obs.obs_properties_add_bool(startup_group, "start_with_obs", "Start automatically with OBS")
    obs.obs_property_set_long_description(auto_start, 
        "If enabled, the projector will automatically start when OBS launches")
    
    startup_delay = obs.obs_properties_add_int(startup_group, "startup_seconds", "Startup delay (seconds)", 5, 3600, 1)
    obs.obs_property_set_long_description(startup_delay,
        "Time to wait before starting the projector. Useful if your system needs time to initialize displays")
    
    # Add display options group
    display_group = obs.obs_properties_create()
    obs.obs_properties_add_group(props, "display_group", "Display Options", obs.OBS_GROUP_NORMAL, display_group)
    
    # Add monitor selection with detailed information
    monitors = obs.obs_properties_add_list(display_group, "monitor", "Monitor", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_INT)
    obs.obs_property_set_long_description(monitors,
        "Select the display where you want to show the projector")
    
    # Add monitors with detailed information
    screen_info = get_screen_info()
    for screen in screen_info:
        # Add monitor with name and description
        display_text = f"{screen['name']} - {screen['description']}"
        obs.obs_property_list_add_int(monitors, display_text, screen['index'])
    
    # Add test button for monitor
    test_button = obs.obs_properties_add_button(display_group, "test_projector", "Test Selected Monitor (3s)", start_test_projector)
    obs.obs_property_set_long_description(test_button,
        "Shows a test pattern on the selected monitor for 3 seconds")
    
    # Add projector options group
    projector_group = obs.obs_properties_create()
    obs.obs_properties_add_group(props, "projector_group", "Projector Options", obs.OBS_GROUP_NORMAL, projector_group)
    
    # Add projector type selection with callback
    proj_type = obs.obs_properties_add_list(projector_group, "projector_type", "Projector Type", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_set_long_description(proj_type,
        "Preview: Shows the preview window\nScene: Shows a specific scene")
    obs.obs_property_list_add_string(proj_type, "Preview", "preview")
    obs.obs_property_list_add_string(proj_type, "Scene", "scene")
    obs.obs_property_set_modified_callback(proj_type, on_projector_type_changed)
    
    # Add scene selection with refresh button
    scenes = obs.obs_properties_add_list(projector_group, "scene", "Scene", obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
    obs.obs_property_set_long_description(scenes,
        "Select which scene to display when using Scene projector type")
    scene_names = get_scene_names()
    for scene in scene_names:
        obs.obs_property_list_add_string(scenes, scene, scene)
    
    refresh_button = obs.obs_properties_add_button(projector_group, "refresh_scenes", "Refresh Scene List", refresh_scene_list)
    obs.obs_property_set_long_description(refresh_button,
        "Click to update the list of available scenes")

    # Add information text
    info_text = (
        "This plugin allows you to automatically start a fullscreen projector on any monitor.\n"
        "You can choose between showing the preview or a specific scene.\n"
        "Use the hotkey (configurable in OBS settings) to toggle the projector.\n\n"
        " TheGeekFreaks 2025"
    )
    info = obs.obs_properties_add_text(props, "info", info_text, obs.OBS_TEXT_INFO)

    return props

def get_screen_info():
    """Get screen information with detailed monitor names"""
    screens = []
    
    # On Windows, try pywin32 first
    if platform.system().lower() == 'windows':
        try:
            from win32api import EnumDisplayMonitors, GetMonitorInfo, GetSystemMetrics
            
            def callback(monitor, dc, rect, data):
                try:
                    info = GetMonitorInfo(monitor)
                    device = info['Device'].replace('\\\\.\\', '') # Clean up device name
                    is_primary = info['Flags'] == 1
                    width = rect[2] - rect[0]
                    height = rect[3] - rect[1]
                    position = info['Monitor']
                    x, y = position[0], position[1]
                    
                    # Format monitor information
                    desc = (f"{device} - {width}x{height} at ({x},{y})"
                           f"{' (Primary)' if is_primary else ''}")
                    
                    # Store both display name and description
                    screens.append({
                        'index': len(screens),
                        'name': f"Monitor {len(screens) + 1}",
                        'description': desc,
                        'device': device,
                        'width': width,
                        'height': height,
                        'is_primary': is_primary
                    })
                except Exception as e:
                    logging.error(f"Error processing monitor info: {str(e)}")
                return True
            
            EnumDisplayMonitors(None, None, callback, None)
            
            if screens:
                logging.info(f"Successfully detected {len(screens)} monitors using win32api")
                return screens
            else:
                logging.warning("No monitors detected with win32api")
        except Exception as e:
            logging.error(f"Win32api monitor detection failed: {str(e)}")
    
    # Fallback to simpler win32api method if the detailed method failed
    if platform.system().lower() == 'windows':
        try:
            from win32api import GetSystemMetrics
            num_monitors = GetSystemMetrics(80)  # SM_CMONITORS
            logging.info(f"Detected {num_monitors} monitors using simple win32api method")
            return [{
                'index': i,
                'name': f"Monitor {i + 1}",
                'description': f"Display {i + 1}",
                'device': f"DISPLAY{i+1}",
                'width': GetSystemMetrics(0),
                'height': GetSystemMetrics(1),
                'is_primary': (i == 0)
            } for i in range(num_monitors)]
        except Exception as e:
            logging.error(f"Simple win32api monitor detection failed: {str(e)}")
    
    # Final fallback
    screens = [{
        'index': i,
        'name': f"Monitor {i + 1}",
        'description': "Unknown Display",
        'device': f"DISPLAY{i+1}",
        'width': 1920,
        'height': 1080,
        'is_primary': (i == 0)
    } for i in range(7)]  # Maximum of 7 monitors in fallback mode
    
    logging.info("Using basic fallback monitor detection (limited to 7 monitors)")
    return screens