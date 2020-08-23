
import pygame
import time

from ui.event import EventBox
from ui import colors
from ui import textwrap
from ui.factory import FactoryBox
from ui.offbooks import OffBooksProducerBox

class Window:
    def __init__(self, screen, width, height, fontsizes):
        self.screen = screen
        self.width = width
        self.height = height

        self.game_data = None

        self.event_list = []
        self.event_height = height // 11
        self.event_width = width // 5
        self.event_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes["events"]
        )
        self.event_surface = pygame.Surface((self.event_width, height))
        self.event_surface_pos = (width-self.event_width, 0)
        self.event_xpos = self.event_surface_pos[0]
        self.oldest_event = None

        # width of left part of screen
        self.left_width = width - self.event_width

        # infobar
        self.info_font = pygame.font.Font(
            'freesansbold.ttf',
            fontsizes["info"]
        )
        self.infobar_height = height // 29
        self.info_pad = (self.infobar_height - fontsizes["info"]) // 2
        self.infobar_surface = pygame.Surface((self.left_width, self.infobar_height))
        renown_width = self.left_width // 4
        self.infobar_renown_rect = pygame.Rect(self.info_pad, self.info_pad, renown_width, self.infobar_height)
        self.infobar_cash_rect = pygame.Rect(
            (
                renown_width,
                self.info_pad, 
                self.left_width - (self.left_width // 4),
                self.infobar_height
            )
        )

        # stock area
        

        # production area
        self.production_cost = None
        self.production_rate = None
        self.production_height = (height - self.infobar_height) // 2
        self.production_ypos = self.production_height + self.infobar_height
        self.production_width = self.left_width //3 * 2
        self.production_surface = pygame.Surface((self.production_width, self.production_height))

        # Production title
        self.production_title_height = self.infobar_height
        self.production_title_rect = pygame.Rect(
           self.info_pad, self.info_pad, self.production_width, self.infobar_height
        )

        self.production_box_height = (self.production_height - self.production_title_height) // 3
        self.production_box_dimensions = (self.left_width // 3, self.production_box_height)
        
        self.mask_factory = FactoryBox(
            self.production_surface,
            self.production_box_dimensions, 
            "Mask Factories", 
            self.info_font, 
            pos=(0, 0)
        )
        
        self.glove_factory = FactoryBox(self.production_surface, self.production_box_dimensions, "Glove Factories", self.info_font, pos=(0, self.production_box_height))
        self.antibac_factory = FactoryBox(self.production_surface, self.production_box_dimensions, "Antibac Factories", self.info_font, pos=(0, self.production_box_height * 2))
        self.visir_factory = FactoryBox(self.production_surface, self.production_box_dimensions, "Visir Factories", self.info_font, pos=(self.left_width // 3, 0))
        self.ventilator_factory = FactoryBox(self.production_surface, self.production_box_dimensions, "Ventilator Factories", self.info_font, pos=(self.left_width // 3, self.production_box_height))
        self.toilet_paper_factory = FactoryBox(self.production_surface, self.production_box_dimensions, "Toilet paper Factories", self.info_font, pos=(self.left_width // 3, self.production_box_height * 2 ))

        for e in [
            self.mask_factory, self.glove_factory, self.antibac_factory, self.visir_factory, self.ventilator_factory, self.toilet_paper_factory
        ]:
            e.pos = (e.pos[0], e.pos[1]+self.production_title_height)

        # Off-the-books area
        self.offbooks_height = self.production_height
        self.offbooks_width = self.left_width-self.production_width
        self.offbooks_ypos = self.production_ypos
        self.offbooks_xpos = self.production_width
        self.offbooks_surface = pygame.Surface((self.offbooks_width, self.offbooks_height))

        # Off-the-boox title
        self.offbooks_title_height = self.infobar_height
        self.offbooks_title_rect = pygame.Rect(
           self.info_pad, self.info_pad, self.offbooks_width, self.offbooks_title_height
        )
        
        # off-the-books boxes
        self.offbooks_box_dimensions = (
            self.offbooks_width, (self.offbooks_height-self.offbooks_title_height) // 2
        )
        self.offbooks_moonshiners = OffBooksProducerBox(
            self.offbooks_surface, self.offbooks_box_dimensions,
            "Moonshiners producing cheap Antibac",
            self.info_font,
            pos=(0,self.offbooks_title_height)
        )
        self.offbooks_child_labor = OffBooksProducerBox(
            self.offbooks_surface, self.offbooks_box_dimensions,
            "Child labor mask production",
            self.info_font,
            pos=(0,self.offbooks_title_height+self.offbooks_box_dimensions[1])
        )

    def add_event(self, event):
        self.event_list.append(
            EventBox(
                self.event_surface,
                (self.event_width, self.event_height),
                event,
                self.event_font
            )
        )
    
    def pop_event(self):
        """Removes oldest event and blacks event area"""
        self.event_list = self.event_list[1:]
        self.event_surface.fill(colors.DARKER_GRAY)

    def update_gamedata(self, data):
        self.game_data = data


    def draw(self):
        # remove oldest event if old
        if self.event_list:
            if time.time() - self.event_list[0].created > 3:
                self.pop_event()

        self.event_surface.fill(colors.DARKER_GRAY)

        # Add event area at right edge of screen
        for i in range(len(self.event_list)):
            if i > 10: # max 10 events on screen
                break
            self.event_list[i].pos = (0, self.event_height*i)
            self.event_list[i].draw()
        self.screen.blit(self.event_surface, self.event_surface_pos)

        # info bar
        self.infobar_surface.fill(colors.DARK_GRAY)
        if not self.game_data:
            renown = "Renown: 50%"
            cash = "Cash: $1000"
        else:
            renown = f"Renown: {self.game_data['renown']}%"
            cash = f"Cash: ${self.game_data['cash']}"

        textwrap.draw_text(
            self.infobar_surface, 
            renown,
            colors.WHITE,
            self.infobar_renown_rect,
            self.info_font,
        )

        textwrap.draw_text(
            self.infobar_surface, 
            cash,
            colors.WHITE,
            self.infobar_cash_rect,
            self.info_font,
        )
        self.screen.blit(self.infobar_surface, (0, 0))

        # Production Area
        self.production_surface.fill(colors.PRODUCTION_BG)
        textwrap.draw_text(
            self.production_surface,
            "Factories (click to buy more)",
            colors.WHITE,
            self.production_title_rect,
            self.info_font,
        )


        # Mask
        self.mask_factory.production = self.game_data["mask factories"] * self.production_rate["mask factories"]
        self.mask_factory.cost = self.production_cost["mask factories"]
        self.mask_factory.draw()
        
        # Glove
        self.glove_factory.production = self.game_data["glove factories"] * self.production_rate["glove factories"]
        self.glove_factory.cost = self.production_cost["glove factories"]
        self.glove_factory.draw()
        
        # Antibac
        self.antibac_factory.production = self.game_data["antibac factories"] * self.production_rate["antibac factories"]
        self.antibac_factory.cost = self.production_cost["antibac factories"]
        self.antibac_factory.draw()

        # Visir
        self.visir_factory.production = self.game_data["visir factories"] * self.production_rate["visir factories"]
        self.visir_factory.cost = self.production_cost["visir factories"]
        self.visir_factory.draw()

        # Ventilator
        self.ventilator_factory.production = self.game_data["ventilator factories"] * self.production_rate["ventilator factories"]
        self.ventilator_factory.cost = self.production_cost["ventilator factories"]
        self.ventilator_factory.draw()

        # Toilet paper
        self.toilet_paper_factory.production = self.game_data["toilet-paper factories"] * self.production_rate["toilet-paper factories"]
        self.toilet_paper_factory.cost = self.production_cost["toilet-paper factories"]
        self.toilet_paper_factory.draw()

        # Blit
        self.screen.blit(self.production_surface, (0, self.production_ypos))


        # offbooks drawing
        self.offbooks_surface.fill(colors.OFFBOOKS_BG)
        textwrap.draw_text(
            self.offbooks_surface,
            "Off the books",
            colors.OFFBOOKS_TITLE,
            self.offbooks_title_rect,
            self.info_font,
        )
        self.offbooks_moonshiners.production = self.game_data["moonshiner factories"] * self.production_rate["moonshiner factories"]
        self.offbooks_moonshiners.cost = self.production_cost["moonshiner factories"]
        self.offbooks_moonshiners.draw()

        self.offbooks_child_labor.production = self.game_data["childlabor factories"] * self.production_rate["childlabor factories"]
        self.offbooks_child_labor.cost = self.production_cost["childlabor factories"]
        self.offbooks_child_labor.draw()

        self.screen.blit(self.offbooks_surface, (self.offbooks_xpos, self.offbooks_ypos))

    def update_production_data(self, cost, rate):
        self.production_cost = cost
        self.production_rate = rate