import json
import random
from time import sleep
from typing import List

import dt_tools.net.net_helper as nh
from loguru import logger as LOGGER

from hubspace_da.api_interface import HubSpaceAPI


class HubspaceSwitchDevice():
    def __init__(self, hs: HubSpaceAPI, child_id: str):
        self._hs = hs
        _, model, device_id, device_class, friendly_name = self._hs.getChildInfoById(child_id)
        self._child_id = child_id
        self._model = model
        self._device_id = device_id
        self._device_class = device_class
        self._friendly_name = friendly_name
        self._wifi_ssid = None
        self._wifi_mac_address = None
        self._wifi_ip_address = None
        self._available = None
        self._bluetooth_mac_address = None
        self._func_instances: list[str] = None
        LOGGER.debug(f'HubspaceSwitchDevice {friendly_name} created.')

    @property
    def name(self):
        """Return friendly_name"""
        return self._friendly_name
    @property
    def child_id(self):
        """Return child_id"""
        return self._child_id
    @property
    def model(self):
        """Return device model"""
        return self._model
    @property
    def device_id(self):
        """Return device_id"""
        return self._device_id
    @property
    def device_class(self):
        """Return class of device"""
        return self._device_class
    
    @property
    def wifi_ssid(self):
        if self._wifi_ssid is None:
            self._wifi_ssid = self._get_debug_field('wifi-ssid')
        return self._wifi_ssid
        
    @property
    def wifi_mac_address(self):
        if self._wifi_mac_address is None:
            self._wifi_mac_address = self._get_debug_field('wifi-mac-address')
        return self._wifi_mac_address
    
    @property
    def wifi_ip_address(self):
        if self._wifi_ip_address is None or self._wifi_ip_address == '1.1.1.1':
            try:
                self._wifi_ip_address = nh.get_ip_from_mac(self.wifi_mac_address)
            except:
                self._wifi_ip_address = '1.1.1.1'

        return self._wifi_ip_address
    
    @property
    def available(self) -> bool:
        is_available = self._get_debug_field('available')
        return is_available

    @property
    def bluetooth_mac_address(self) -> bool:
        if self._bluetooth_mac_address is None:
            self._bluetooth_mac_address = self._get_debug_field('ble-mac-address')
        return self._bluetooth_mac_address
    
    @property 
    def instances(self) -> List[str]:
        """Return list of (toggle) instances for this HubspaceSwitchDevice"""
        if self._func_instances is None:
            self._func_instances = []
            debug_info = self._hs.getDebugInfo(self.child_id)
            LOGGER.trace(f'{self.name} - debug_info: {debug_info}\n')
            if debug_info.get('metadeviceId') == self.child_id:
                for func_dict in debug_info.get('values'):
                    LOGGER.trace(f'{self.name} - func_dict: {func_dict}\n')
                    if func_dict.get('functionClass') == 'toggle':
                        func_instance = func_dict.get('functionInstance')
                        LOGGER.trace(f'{self.name} - func_instance: {func_instance}\n')
                        if not func_instance is None:
                            if not func_instance in self._func_instances:
                                self._func_instances.append(func_instance)
            LOGGER.debug(f'{self.name}- {len(self._func_instances)} lazy loaded.')
                            
        return self._func_instances

    # ---------------------------------------------------------------------------------    
    def to_json(self, formatted: bool = False) -> dict:
        instance_list = []
        for inst in self.instances:
            entry = {'name': inst, 'state': self.get_power_state(inst)}
            instance_list.append(entry)

        token=  {
            "child_id": self.child_id,
            "friendly_name": self.name,
            "model": self.model,
            "class": self.device_class,
            "instances": instance_list
        }
        if formatted:
            return json.dumps(token, indent=2)
            
        return json.dumps(token)


    def get_power_state(self, instance_name: str = None) -> str:
        """Get switch (or switch instance) power state (on/off)"""
        power_state = None
        if instance_name:
            if instance_name in self.instances:
                power_state = self._hs.getStateInstance(self.child_id, 'toggle', instance_name )
        else:
            power_state = self._hs.getState(self.child_id, 'power')
        return power_state
    
    def turn_on(self, instance_name: str = None) -> bool:
        """Turn on switch (or switch instance)"""
        LOGGER.info(f'{self._friendly_name}: turn_on [{instance_name}]')        
        power_state = self.get_power_state(instance_name)
        if power_state is None:
            raise KeyError(f'Instance {instance_name} not found/valid.')
        
        if power_state == "off":
            if instance_name:
                self._hs.setStateInstance(self.child_id, 'toggle', instance_name, "on")
            else:
                self._hs.setState(self.child_id, 'power', "on")
            LOGGER.info(f'{self._friendly_name} - sent on request.')
        else:
            LOGGER.warning(f'{self.name} [{instance_name}] already turned on.')
        
        return True

    def turn_off(self, instance_name: str = None) -> bool:
        """Turn of switch (or switch instance)"""
        LOGGER.info(f'{self._friendly_name}: turn_off [{instance_name}]')        
        power_state = self.get_power_state(instance_name)        
        if power_state is None:
            raise KeyError(f'Instance {instance_name} not found/valid.')
        
        if power_state == "on":
            if instance_name:
                self._hs.setStateInstance(self.child_id, 'toggle', instance_name, "off")
            else:
                self._hs.setState(self.child_id, 'power', "off")
            LOGGER.info(f'{self._friendly_name} - sent off request.')
        else:
            LOGGER.warning(f'{self.name} [{instance_name}] already turned off.')
        
        return True


    def get_debug_info(self) -> dict:
        debug_info = self._hs.getDebugInfo(self.child_id)
        return debug_info
        

    def _get_debug_field(self, function_class: str, instance_name: str = None):
        ret_value = None
        debug_info = self._hs.getDebugInfo(self.child_id)
        if debug_info.get('metadeviceId') == self.child_id:
            for value_dict in debug_info.get('values'):
                if value_dict.get('functionClass') == function_class:
                    if instance_name is None or value_dict.get("functionInstance") == instance_name:
                        ret_value = value_dict.get('value')
                        break
        return ret_value
    



class HubspaceManager():
    def __init__(self, userid: str, password: str):
        self._initialized:bool = False
        self._devices: list[HubspaceSwitchDevice] = None
        try:
            self._hs = HubSpaceAPI(userid, password)
            self._initialized = True
        except Exception as ex:
            LOGGER.warning(f'Unable to initialize HubspaceAPI: {repr(ex)}')

        # retry = 0
        # max_retries = 3
        # while not self._initialized and retry < max_retries:
        #     try:
        #         self._hs = HubSpaceAPI(userid, password)
        #         self._initialized = True
        #     except Exception as ex:
        #         LOGGER.debug(f'Unable to initialize HubspaceAPI: {repr(ex)} [{retry}]')
        #         sleep(random.choice([1.0, 1.5, 2.0, 2.5]))
        #         retry += 1
            
        if self._initialized:
            LOGGER.debug('HubspaceManager created.')
        else:
            LOGGER.debug('HubspaceManager created, but NOT initialized.')

    @property
    def initialized(self) -> bool:
        return self._initialized
    
    @property
    def devices(self) -> List[HubspaceSwitchDevice]:
        """Return list of HubspaceSwitchDevice"""
        if self._devices is None and self.initialized:
            self._devices = []
            device_ids = self._hs.discoverDeviceIds()
            for item in device_ids:
                child_id = item[0]
                model = item[1]
                device_id = item[2]
                device_class = item[3]
                friendly_name = item[4]
                functions = item[5]                
                device = HubspaceSwitchDevice(self._hs, child_id)
                self._devices.append(device)
            LOGGER.debug(f'HubspaceManager - {len(self._devices)} devices lazy loaded.')

        return self._devices
    

    def get_device(self, name_or_id: str) -> HubspaceSwitchDevice:
        """Return device associated with friendly name or child_id"""
        for dev in self.devices:
            if dev.name == name_or_id or dev.child_id == name_or_id:
                return dev
            
        LOGGER.error(f'Unable to locate device: {name_or_id}')
        return None
    
    def dump_devices(self):
        LOGGER.info('in dump_devices')
        if self._initialized:
            device_ids = self._hs.discoverDeviceIds()
            for device in device_ids:
                child = device[0]
                model = device[1]
                device_id = device[2]
                device_class = device[3]
                friendly_name = device[4]
                functions = device[5]
                LOGGER.info('== Device===================================================================')
                LOGGER.info(f'Child         : {child}')
                LOGGER.info(f'Model         : {model}')
                LOGGER.info(f'Device Id     : {device_id}')
                LOGGER.info(f'Device Class  : {device_class}')
                LOGGER.info(f'Friendly Name : {friendly_name}')
                func_cnt = 0
                for function in functions:
                    func_cnt += 1
                    LOGGER.info(f'{friendly_name}: function({func_cnt})\n{json.dumps(function,indent=2,)}')
                   