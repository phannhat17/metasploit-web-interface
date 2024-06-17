import json
import xmltodict
import datetime
import os

def convert_xml_to_json(xml_file_path):
    """
    Converts an XML file to a JSON file, using the 'startstr' timestamp in the XML 
    for naming the JSON file. Saves the JSON file in the same directory as the XML file
    and deletes the XML file after conversion.

    Args:
    xml_file_path (str): Path to the XML file to be converted.

    Returns:
    str: Path to the created JSON file or None if an error occurred.
    """
    try:
        # Open and read the XML file
        with open(xml_file_path, "r") as file:
            xml_content = file.read()

        # Parse the XML content to JSON
        json_data = xmltodict.parse(xml_content)

        # Extract the 'startstr' attribute from the 'nmaprun' element
        start_str = json_data['nmaprun']['@startstr']

        # Convert the 'startstr' string to a datetime object
        date_object = datetime.datetime.strptime(start_str, "%a %b %d %H:%M:%S %Y")

        # Format the datetime object into a string suitable for the filename
        formatted_time = date_object.strftime("%Y%m%d%H%M%S")

        # Extract the directory path from the xml_file_path
        directory_path = os.path.dirname(xml_file_path)

        # Define the JSON output file name with the timestamp in the same directory
        json_file_name = os.path.join(directory_path, f"{formatted_time}.json")

        # Write the JSON data to a file
        with open(json_file_name, "w") as json_file:
            json.dump(json_data, json_file, indent=4, sort_keys=True)

        # Delete the original XML file after successful conversion
        os.remove(xml_file_path)
        return json_file_name

    except Exception as e:
        return None
