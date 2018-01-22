#!/usr/bin/python

from argparse import ArgumentParser
import os
import minid_client.minid_client_api as mca


class MINIDIntegration(object):
    def __init__(self, 
                 register=False, 
                 register_user=False, 
                 update=False, 
                 test=False, 
                 json=True, 
                 title=None, 
                 locations=None, 
                 status=None, 
                 obsoleted_by=None,
                 content_key=None, 
                 config=None, 
                 email=None,
                 name=None,
                 orcid=None,
                 code=None,
                 globus_auth_token=None,
                 quiet=None,
                 filename=None
                 ):

        self.register = register           
        self.register_user = register_user
        self.update = update
        self.test = test
        self.json = json
        self.title = title
        self.locations = locations
        self.status = status
        self.obsoleted_by = obsoleted_by
        self.content_key = content_key
        self.config = config
        self.email = email
        self.name = name
        self.orcid = orcid
        self.code = code
        self.globus_auth_token = globus_auth_token
        self.quiet = quiet
        self.filename = filename
        if __name__ == '__main__':
            self.main()
        
    def _main(self):
        
        if not self.quiet:
            mca.configure_logging()
    
        config = mca.parse_config(self.config)
    
        server = config["minid_server"]
        if self.server:
            server = self.server
    
        entities = None
    
        # register a new user
        if self.register_user:
            mca.register_user(server, self.email, self.name, self.orcid,
                              self.globus_auth_token)
            return
    
        # if we got this far we *must* have a filename (or identifier) arg
        if not self.filename:
            print("Either a file name or an identifier must be specified.")
            return
    
        # see if this file or name exists
        file_exists = os.path.isfile(self.filename)
        if file_exists:
            checksum = mca.compute_checksum(self.filename)
            entities = mca.get_entities(server, checksum, self.test)
        else:
            entities = mca.get_entities(server, self.filename, False)
            if entities is None:
                print("No entity registered with identifier: %s" % self.filename)
                return
       
        # register file or display info about the entity
        if self.register:
            if entities and not file_exists:
                print("You must use the --update command to update a minid")
                return
            else:
                locations = self.locations
                if locations is None or len(locations) ==0:
                    if "local_server" in config:
                        locations = ["%s%s" % (config["local_server"], os.path.abspath(self.filename))]
                mca.register_entity(server,
                                    checksum,
                                    self.email if self.email else config["email"],
                                    self.code if self.code else config["code"],
                                    locations, self.title, self.test, self.content_key,
                                    self.globus_auth_token)
        elif self.update:
            if entities is None:
                print("No entity found to update. You must use a valid minid.")
                return
            elif len(entities) > 1:
                print("More than one minid identified. Please use a minid identifier")
            else:
                entity = list(entities.values())[0]
                if self.status:
                    entity['status'] = self.status
                if self.obsoleted_by:
                    entity['obsoleted_by'] = self.obsoleted_by
                if self.title:
                    entity['titles'] = [{"title" : self.title}]
                if self.locations:
                    locs = []
                    for l in self.locations:
                        locs.append({'uri': l})
                    entity['locations'] = locs
    
                updated_entity = mca.update_entity(server,
                                                   self.filename,
                                                   entity,
                                                   self.email if self.email else config["email"],
                                                   self.code if self.code else config["code"],
                                                   self.globus_auth_token)
                print(updated_entity)
        else:
            if entities:
                mca.print_entities(entities, self.json)
            else:
                print("File is not named. Use --register to create a name for this file.")
    
    def main(self):
        try:
            self._main()
        except mca.MinidAPIException:
            pass


