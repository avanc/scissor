from . import decoder


def OtrDecoder(config):
    otrdecoder=decoder.OtrDecoder(config["email"], config["password"])
    if ("working_dir" in config):
        otrdecoder.output_path=config["working_dir"]
    if ("otrdecoder" in config):
        otrdecoder.executable=config["otrdecoder"]
        
    return otrdecoder
        
    
    
